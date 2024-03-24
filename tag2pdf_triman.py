from PyPDF2.generic import RectangleObject
from PyPDF2 import PdfReader, PdfWriter, Transformation

reader = PdfReader("txm.pdf")
merger = PdfWriter()
new_page = reader.pages[0]
num_per_page = 39
num_per_row = 3
i=0
total_tags = int(2*len(reader.pages) / num_per_page + 1) * num_per_page
current_barcode_index = 1
switch2triman_yn = -1
y_n = 0
x_n = 0
for i in range(1, total_tags):
    if(current_barcode_index>=len(reader.pages)):
        break
    if(i % num_per_page == 0):
        # 一页已经满了，保存当前页
        merger.add_page(new_page)
        new_page = reader.pages[current_barcode_index]
        current_barcode_index += 1
        continue
    y_n = -int(i%num_per_page / num_per_row)
    x_n = i % num_per_row
    p1 = reader.pages[current_barcode_index]
    if(abs(y_n) % 2 == 1):
        #奇数行打印 triman 标签，同时不更新current_barcode_index
        triman_reader = PdfReader("images/triman.pdf")
        p1 = triman_reader.pages[0]
    else:
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

if(x_n != 0):
    y_n -= 1
    for i in range(0, x_n+1):
        triman_reader = PdfReader("images/triman.pdf")
        p1 = triman_reader.pages[0]
        length = p1.cropbox.right
        height = p1.cropbox.top
        op1 = Transformation().translate(tx=i*length, ty=y_n*height)
        p1.add_transformation(op1)
        cb = p1.cropbox
        p1.mediabox = RectangleObject((cb.left+i*length, cb.bottom+y_n*height,
                                    cb.right+i*length, cb.top+y_n*height))
        p1.cropbox = RectangleObject((cb.left+i*length, cb.bottom+y_n*height,
                                    cb.right+i*length, cb.top+y_n*height))
        p1.trimbox = RectangleObject((cb.left+i*length, cb.bottom+y_n*height,
                                    cb.right+i*length, cb.top+y_n*height))
        p1.bleedbox = RectangleObject((cb.left+i*length, cb.bottom+y_n*height,
                                    cb.right+i*length, cb.top+y_n*height))
        p1.artbox = RectangleObject((cb.left+i*length, cb.bottom+y_n*height,
                                    cb.right+i*length, cb.top+y_n*height))
        new_page.merge_page(p1,expand=True)
        m_mb = new_page.mediabox
        new_page.mediabox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
        new_page.cropbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
        new_page.trimbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
        new_page.bleedbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))
        new_page.artbox = RectangleObject((m_mb.left, m_mb.bottom, m_mb.right, m_mb.top))

# Write to an output PDF document
merger.add_page(new_page)
with open("triman_output.pdf", "wb") as fp:
    merger.write(fp)