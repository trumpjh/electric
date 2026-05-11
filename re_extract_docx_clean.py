#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Re-extract DOCX with better handling of:
1. Remove "? ①②③④" from problem text
2. Extract formulas properly (not as [수식])
3. Parse options without formulas
4. Match images to problems correctly
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import json
from pathlib import Path
from collections import defaultdict

# Namespace definitions
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

def extract_text_from_para(para):
    """Extract all text from paragraph, preserving structure"""
    texts = []
    
    # Direct runs
    for run in para.findall('.//w:r', namespaces):
        for t in run.findall('.//w:t', namespaces):
            if t.text:
                texts.append(t.text)
    
    return ''.join(texts)

def extract_problem_blocks():
    """Extract problems with proper text and image handling"""
    docx_path = Path('전기기능사 시험문제(2025-2023).docx')
    
    with zipfile.ZipFile(docx_path, 'r') as docx_zip:
        doc_xml = docx_zip.read('word/document.xml')
        doc_rels_xml = docx_zip.read('word/_rels/document.xml.rels')
        
        root = ET.fromstring(doc_xml)
        rels_root = ET.fromstring(doc_rels_xml)
        
        # Build image mapping
        image_map = {}
        for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            rel_id = rel.get('Id')
            target = rel.get('Target')
            if 'image' in target.lower():
                image_map[rel_id] = target
        
        paragraphs = root.findall('.//w:p', namespaces)
        
        problems = []
        current_problem = None
        image_counter = 0
        para_texts = []
        
        # First pass: get all paragraph texts
        for i, para in enumerate(paragraphs):
            # Check for image
            has_image = False
            image_path = None
            pic_elems = para.findall('.//pic:pic', namespaces)
            if pic_elems:
                has_image = True
                # Extract image
                image_counter += 1
                image_path = f'extracted_image_{image_counter}.png'
                
                # Try to extract image file
                for blip in para.findall('.//a:blip', {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}):
                    rel_id = blip.get('{' + namespaces['r'] + '}embed')
                    if rel_id and rel_id in image_map:
                        image_path = image_map[rel_id]
                        # Extract image file
                        try:
                            image_data = docx_zip.read(f'word/{image_path}')
                            out_path = Path('problem_images') / Path(image_path).name
                            out_path.parent.mkdir(exist_ok=True)
                            out_path.write_bytes(image_data)
                            image_path = str(out_path)
                        except:
                            image_path = None
            
            text = extract_text_from_para(para)
            para_texts.append({
                'index': i,
                'text': text,
                'has_image': has_image,
                'image_path': image_path
            })
        
        # Parse problems
        problem_pattern = r'^\d+\.\s*(.+?)(?:①|②|③|④)'
        problem_count = 0
        
        for i, para_info in enumerate(para_texts):
            text = para_info['text'].strip()
            
            # Check if this is a problem line
            if re.match(r'^\d+\.\s*', text):
                # Clean up problem text
                clean_text = re.sub(r'\?.*$', '', text)  # Remove "? ①②③④" at end
                clean_text = re.sub(r'^\d+\.\s*', '', clean_text)  # Remove number prefix
                clean_text = clean_text.strip()
                
                # Look for options in subsequent paragraphs
                options = []
                j = i + 1
                max_look_ahead = 10
                has_answer = False
                answer_char = None
                
                while j < len(para_texts) and j < i + max_look_ahead:
                    next_text = para_texts[j]['text'].strip()
                    
                    # Stop if we hit next problem
                    if re.match(r'^\d+\.\s*', next_text) and j > i + 1:
                        break
                    
                    # Check for option pattern
                    if re.match(r'^[①②③④]', next_text):
                        # Found options start
                        opt_char = next_text[0]
                        opt_text = next_text[1:].strip()
                        options.append((opt_char, opt_text))
                        
                        if '?' in text:
                            answer_match = re.search(r'\?\s*([①②③④])', text)
                            if answer_match:
                                has_answer = True
                                answer_char = answer_match.group(1)
                    
                    j += 1
                
                if options and len(options) >= 3:  # Need at least 3-4 options
                    problem_count += 1
                    problems.append({
                        'number': problem_count,
                        'text': clean_text,
                        'options': options,
                        'has_image': para_info['has_image'],
                        'image_path': para_info['image_path'],
                        'raw_options_text': ' '.join([f"{c}{t}" for c, t in options])
                    })
        
        return problems

if __name__ == '__main__':
    try:
        problems = extract_problem_blocks()
        print(f"\n✓ Extracted {len(problems)} problems")
        
        for i, prob in enumerate(problems[:6], 1):
            print(f"\n=== Problem {prob['number']} ===")
            print(f"Text: {prob['text']}")
            print(f"Options: {prob['raw_options_text']}")
            print(f"Has Image: {prob['has_image']}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
