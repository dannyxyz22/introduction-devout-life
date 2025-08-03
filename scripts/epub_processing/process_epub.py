import json
import re
import os
from bs4 import BeautifulSoup

file_order = [
    os.path.join('OEBPS', 'content', 'content-0012.xml'),
    os.path.join('OEBPS', 'content', 'content-0013.xml'),
    os.path.join('OEBPS', 'content', 'content-0017.xml'),
    os.path.join('OEBPS', 'content', 'content-0019.xml'),
    os.path.join('OEBPS', 'content', 'content-0022.xml'),
    os.path.join('OEBPS', 'content', 'content-0025.xml')
]

book_structure = []

# Mapeamento de títulos de partes para os arquivos correspondentes
part_titles = {
    'content-0012.xml': "PART THE FIRST. INSTRUCTIONS AND EXERCISES FOR CONDUCTING THE SOUL FROM HER FIRST DESIRE FOR A DEVOUT LIFE TILL SHE IS BROUGHT TO A FULL RESOLUTION OF EMBRACING IT.",
    'content-0013.xml': "PART THE SECOND. CONTAINING DIVERS INSTRUCTIONS FOR THE ELEVATION OF THE SOUL TO GOD BY PRAYER AND THE USE OF THE SACRAMENTS.",
    'content-0017.xml': "PART THE THIRD. CONTAINING MANY INSTRUCTIONS ON THE PRACTICE OF VIRTUE.",
    'content-0019.xml': "PART THE THIRD. (CONTINUATION)",
    'content-0022.xml': "PART THE FOURTH. CONTAINING NECESSARY INSTRUCTIONS AGAINST THE MOST USUAL TEMPTATIONS.",
    'content-0025.xml': "PART THE FIFTH. CONTAINING EXERCISES AND INSTRUCTIONS FOR RENEWING THE SOUL AND CONFIRMING HER IN DEVOTION."
}

for file_path in file_order:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # Usa o título do dicionário
    part_title = part_titles.get(os.path.basename(file_path), "Untitled Part")
    
    current_part = {
        "part_title": part_title,
        "chapters": []
    }

    all_elements = soup.find_all(['p', 'div'])
    current_chapter = None

    for element in all_elements:
        # Tenta encontrar um título de capítulo (ex: 'CHAPTER I.')
        text_content = element.get_text().strip()
        is_chapter_title = re.match(r'^CHAPTER\s+[IVXLCDM]+\s*\.?$', text_content, re.IGNORECASE)
        
        if is_chapter_title:
            # O próximo elemento <p> geralmente contém o título descritivo
            next_p = element.find_next_sibling('div')
            if next_p and next_p.find('p'):
                chapter_title_desc = next_p.find('p').get_text(strip=True)
                full_chapter_title = f"{text_content}: {chapter_title_desc}"
            else:
                full_chapter_title = text_content

            current_chapter = {
                "chapter_title": full_chapter_title,
                "content": []
            }
            current_part["chapters"].append(current_chapter)
            continue # Pula para o próximo elemento

        # Se for um parágrafo de texto normal
        if element.name == 'p' and text_content:
            # Se não estamos em um capítulo, cria um capítulo 'Introduction'
            if not current_chapter:
                current_chapter = {
                    "chapter_title": "Introduction",
                    "content": []
                }
                current_part["chapters"].append(current_chapter)

            cleaned_text = re.sub(r'\s+', ' ', text_content).strip()
            if cleaned_text:
                word_count = len(cleaned_text.split())
                current_chapter["content"].append({
                    "type": "p",
                    "content": cleaned_text,
                    "word_count": word_count
                })

    book_structure.append(current_part)

# Salva o arquivo JSON
with open('livro_original.json', 'w', encoding='utf-8') as f:
    json.dump(book_structure, f, indent=2, ensure_ascii=False)

print("Arquivo livro_original.json criado com sucesso.")

# Move as imagens (código mantido)
images_dir = 'images'
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

data_dir = os.path.join('OEBPS', 'data')
if os.path.exists(data_dir):
    image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for img in image_files:
        try:
            source_path = os.path.join(data_dir, img)
            destination_path = os.path.join(images_dir, img)
            os.rename(source_path, destination_path)
        except FileExistsError:
            print(f"A imagem {img} já existe no diretório images/.")

print("Imagens movidas para o diretório images/.")