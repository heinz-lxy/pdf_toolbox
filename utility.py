from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime


def merge_pdf_by_path(src_paths, dst_path):
    pdf_writer = PdfFileWriter()
    page_total = 0
    files = []
    for src_path in src_paths:
        src_file = open(src_path, 'rb')
        files.append(src_file)
        pdf_reader = PdfFileReader(src_file)
        page_count = pdf_reader.numPages
        page_total += page_count
        for i in range(page_count):
            pg = pdf_reader.getPage(i)
            pdf_writer.addPage(pg)
    with open(dst_path,'wb') as dst_file:
        pdf_writer.write(dst_file)
    for file in files:
        file.close()


def split_pdf_by_path(src_path, dst_path, page_start, page_end):
    pdf_writer = PdfFileWriter()
    with open(src_path, 'rb') as src_file:
        pdf_reader = PdfFileReader(src_file)
        page_count = pdf_reader.numPages
        for i in range(page_count):
            if ((i+1) >= page_start) and ((i+1) <= page_end):
                pg = pdf_reader.getPage(i)
                pdf_writer.addPage(pg)
        with open(dst_path,'wb') as dst_file:
            pdf_writer.write(dst_file)



def encrypt_pdf_by_path(src_path, dst_path, password):
    pdf_writer = PdfFileWriter()
    with open(src_path, 'rb') as src_file:
        pdf_reader = PdfFileReader(src_file)
        page_count = pdf_reader.numPages
        for i in range(page_count):
            pg = pdf_reader.getPage(i)
            pdf_writer.addPage(pg)
        pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
        with open(dst_path,'wb') as dst_file:
            pdf_writer.write(dst_file)


def decrypt_pdf_by_path(src_path, dst_path, password):
    pdf_writer = PdfFileWriter()
    with open(src_path, 'rb') as src_file:
        pdf_reader = PdfFileReader(src_file)
        pdf_reader.decrypt(password)
        page_count = pdf_reader.numPages
        for i in range(page_count):
            pg = pdf_reader.getPage(i)
            pdf_writer.addPage(pg)
        with open(dst_path,'wb') as dst_file:
            pdf_writer.write(dst_file)


def watermark_pdf_by_path(src_path, dst_path, wmk_path):
    with open(src_path, "rb") as src_file, open(wmk_path, "rb") as wmk_file:
        src_pdf_reader = PdfFileReader(src_file)
        wmk_pdf_reader = PdfFileReader(wmk_file)
        wmk_page = wmk_pdf_reader.getPage(0)
        pdf_writer = PdfFileWriter()
        for i in range(src_pdf_reader.getNumPages()):
            pdf_page = src_pdf_reader.getPage(i)
            pdf_page.mergePage(wmk_page)
            pdf_writer.addPage(pdf_page)
        with open(dst_path, "wb") as dst_file:
            pdf_writer.write(dst_file)


def get_current_time_string():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_filename(file_path):
    seperator = '\\' if '\\' in file_path else '/'
    return file_path.split(seperator)[-1]


if __name__ == '__main__':
    # merge_pdf_by_paths([r'C:\Users\mi\Desktop\新建文件夹\1.pdf', r'C:\Users\mi\Desktop\新建文件夹\2.pdf'], r'C:\Users\mi\Desktop\新建文件夹\3.pdf')
    # encrypt_pdf_by_path(r'C:\Users\mi\Desktop\新建文件夹\1.pdf', r'C:\Users\mi\Desktop\新建文件夹\1_encrypted.pdf', '254731')
    # decrypt_pdf_by_path(r'C:\Users\mi\Desktop\新建文件夹\1_encrypted.pdf', r'C:\Users\mi\Desktop\新建文件夹\1_decrypted.pdf', '254731')
    # watermark_pdf_by_path(r'C:\Users\mi\Desktop\新建文件夹\1.pdf', r'C:\Users\mi\Desktop\新建文件夹\1_watermarked.pdf', r'C:\Users\mi\Desktop\新建文件夹\wmk.pdf')
    split_pdf_by_path(r'C:\Users\mi\Desktop\新建文件夹\1.pdf', r'C:\Users\mi\Desktop\新建文件夹\1_splitted.pdf', 1, 2)






