from PyPDF2.generic import RectangleObject
from PyPDF2 import PdfReader, PdfWriter, Transformation

triman_file_path = "images/triman_2.pdf"
reader = PdfReader("txm.pdf")
merger = PdfWriter()
new_page = reader.pages[0]
num_per_page = 3*14
num_per_row = 3
i=0
total_tags = int(2*len(reader.pages) / num_per_page + 1) * num_per_page
current_barcode_index = 1
switch2triman_yn = -1
y_n = 0
x_n = 0
for i in range(1, total_tags):
    if(i % num_per_page == 0):
        # 一页已经满了，保存当前页
        merger.add_page(new_page)
        if(current_barcode_index<len(reader.pages)):
            new_page = reader.pages[current_barcode_index]
            current_barcode_index += 1
            continue
        else:
            break
    y_n = -int(i%num_per_page / num_per_row)
    x_n = i % num_per_row
    if(abs(y_n) % 2 == 1 or current_barcode_index>=len(reader.pages)):
        #奇数行或者条码已经打印完毕，将剩余部分打印 triman 标签，同时不更新current_barcode_index
        triman_reader = PdfReader(triman_file_path)
        p1 = triman_reader.pages[0]
    else:
        p1 = reader.pages[current_barcode_index]
        current_barcode_index += 1

    length = p1.cropbox.right
    height = p1.cropbox.top
    op1 = Transformation().translate(tx=x_n*length, ty=y_n*height)
    p1.add_transformation(op1)
    cb = p1.cropbox
    p1.mediabox = RectangleObject((cb.left+x_n*length, cb.bottom+y_n*height,
                                   cb.right+x_n*length, cb.top+y_n*height))
    p1.cropbox = RectangleObject((cb.left+x_n*length, cb.bottom+y_n*height,
                                   cb.right+x_n*length, cb.top+y_n*height))
    p1.trimbox = RectangleObject((cb.left+x_n*length, cb.bottom+y_n*height,
                                   cb.right+x_n*length, cb.top+y_n*height))
    p1.bleedbox = RectangleObject((cb.left+x_n*length, cb.bottom+y_n*height,
                                   cb.right+x_n*length, cb.top+y_n*height))
    p1.artbox = RectangleObject((cb.left+x_n*length, cb.bottom+y_n*height,
                                   cb.right+x_n*length, cb.top+y_n*height))
    new_page.merge_page(p1,expand=True)
    m_mb = new_page.mediabox
    new_page.mediabox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
    new_page.cropbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
    new_page.trimbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
    new_page.bleedbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
    new_page.artbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))

with open("triman_output.pdf", "wb") as fp:
    merger.write(fp)