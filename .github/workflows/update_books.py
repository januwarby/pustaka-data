import os
import json
import fitz  # PyMuPDF

def classify_category(title):
    title = title.lower()
    # Sistem pemetaan kata kunci sederhana
    keywords = {
        "Self Improvement": ["filosofi", "teras", "habit", "psikologi", "sukses", "mindset"],
        "Teknologi": ["coding", "programming", "python", "react", "html", "data"],
        "Sastra": ["laskar", "pelangi", "novel", "puisi", "cerpen", "menara"],
        "Sejarah": ["sapiens", "sejarah", "dunia", "kerajaan", "perang"]
    }
    
    for category, tags in keywords.items():
        if any(tag in title for tag in tags):
            return category
    return "Umum" # Kategori default jika tidak ditemukan

def generate_data():
    books = []
    ebooks_dir = 'ebooks'
    covers_dir = 'covers'
    
    if not os.path.exists(covers_dir):
        os.makedirs(covers_dir)

    for filename in os.listdir(ebooks_dir):
        if filename.endswith('.pdf'):
            base_name = os.path.splitext(filename)[0]
            pdf_path = os.path.join(ebooks_dir, filename)
            cover_name = f"{base_name}.jpg"
            cover_path = os.path.join(covers_dir, cover_name)

            # 1. Capture Cover
            author_from_pdf = "Penulis Tidak Diketahui"
            if not os.path.exists(cover_path):
                doc = fitz.open(pdf_path)
                
                # Coba ambil Author dari Metadata PDF (jika ada)
                if doc.metadata.get('author'):
                    author_from_pdf = doc.metadata.get('author')
                
                page = doc.load_page(0)
                pix = page.get_pixmap()
                pix.save(cover_path)
                doc.close()

            # 2. Klasifikasi Otomatis
            category = classify_category(base_name)

            books.append({
                "id": str(len(books) + 1),
                "title": base_name.replace('-', ' ').title(),
                "author": author_from_pdf, # Mengambil dari metadata PDF
                "category": category,      # Hasil klasifikasi judul
                "file_path": f"ebooks/{filename}",
                "cover_url": f"https://raw.githubusercontent.com/januwarby/pustaka-data/master/covers/{cover_name}"
            })

    with open('books.json', 'w') as f:
        json.dump(books, f, indent=2)

if __name__ == "__main__":
    generate_data()