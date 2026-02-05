#!/usr/bin/env python3
"""
포트폴리오를 완전히 독립적인 단일 HTML 파일로 변환
모든 이미지를 base64로 인코딩하여 포함
"""

import base64
import os
import mimetypes
from pathlib import Path

# 작업 디렉토리
BASE_DIR = Path("/Users/gimdonghyeon/Desktop/portfolio")
ASSETS_DIR = BASE_DIR / "assets"
INPUT_HTML = BASE_DIR / "index.html"
OUTPUT_HTML = BASE_DIR / "portfolio_standalone.html"

def get_mime_type(file_path):
    """파일의 MIME 타입 반환"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type
    # 기본값
    ext = file_path.suffix.lower()
    mime_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
    }
    return mime_map.get(ext, 'application/octet-stream')

def encode_image_to_base64(image_path):
    """이미지를 base64 data URI로 인코딩"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    base64_data = base64.b64encode(image_data).decode('utf-8')
    mime_type = get_mime_type(image_path)
    
    return f"data:{mime_type};base64,{base64_data}"

def main():
    print("🚀 포트폴리오 단일 파일 생성 시작...\n")
    
    # HTML 파일 읽기
    print(f"📖 {INPUT_HTML.name} 읽는 중...")
    with open(INPUT_HTML, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 이미지 파일 목록 수집
    image_files = []
    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.startswith('.'):  # .DS_Store 등 제외
                continue
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(BASE_DIR)
                image_files.append((str(rel_path), full_path))
    
    print(f"\n📦 발견된 이미지 파일: {len(image_files)}개")
    
    # 각 이미지를 base64로 변환하고 HTML에서 교체
    for i, (rel_path, full_path) in enumerate(image_files, 1):
        print(f"  [{i}/{len(image_files)}] {rel_path}")
        
        # 이미지를 base64로 인코딩
        data_uri = encode_image_to_base64(full_path)
        
        # HTML에서 경로 교체 (슬래시를 포함한 정확한 경로)
        html_content = html_content.replace(f'"{rel_path}"', f'"{data_uri}"')
        html_content = html_content.replace(f"'{rel_path}'", f"'{data_uri}'")
    
    # 결과 파일 저장
    print(f"\n💾 {OUTPUT_HTML.name} 저장 중...")
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 파일 크기 확인
    original_size = INPUT_HTML.stat().st_size / 1024
    standalone_size = OUTPUT_HTML.stat().st_size / 1024 / 1024
    
    print(f"\n✅ 완료!")
    print(f"   원본 크기: {original_size:.1f} KB")
    print(f"   단일 파일 크기: {standalone_size:.2f} MB")
    print(f"\n📄 생성된 파일: {OUTPUT_HTML.name}")
    print(f"   이 파일을 브라우저에서 바로 열 수 있습니다!")

if __name__ == "__main__":
    main()
