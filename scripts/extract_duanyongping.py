#!/usr/bin/env python3
"""
段永平书籍消化脚本
提取PDF和EPUB文件的内容，生成结构化的知识点
"""

import pdfplumber
import os
import json
from pathlib import Path

def extract_pdf_text(pdf_path):
    """从PDF中提取文本"""
    content = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                content.append({
                    'page': i + 1,
                    'text': text.strip()
                })
    return content

def process_pdf(pdf_path, output_dir):
    """处理单个PDF文件"""
    filename = Path(pdf_path).stem
    print(f"处理: {filename}")

    content = extract_pdf_text(pdf_path)

    # 保存原始文本
    output_file = os.path.join(output_dir, f"{filename}_content.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"  - 提取了 {len(content)} 页")
    return content, filename

if __name__ == "__main__":
    base_dir = "/Users/panxiaoli/Desktop/投资大佬agent知识库"
    raw_dir = os.path.join(base_dir, "raw", "duanyongping")
    output_dir = os.path.join(base_dir, "raw", "duanyongping", "extracted")

    os.makedirs(output_dir, exist_ok=True)

    # PDF文件列表
    pdf_files = [
        "段永平01 段永平投资问答录(投资逻辑篇) (段永平) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "段永平02 段永平投资问答录（商业逻辑篇） (段永平) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "段永平博客文章合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "段永平帖子合集 (段永平) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
    ]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(base_dir, pdf_file)
        if os.path.exists(pdf_path):
            content, filename = process_pdf(pdf_path, output_dir)
        else:
            print(f"文件不存在: {pdf_file}")
