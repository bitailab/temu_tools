from PyPDF2.generic import RectangleObject
from PyPDF2 import PdfReader, PdfWriter, Transformation

reader = PdfReader("package.pdf")
merger = PdfWriter()
new_page = reader.pages[0]
num_per_page = 6
num_per_row = 2
for i in range(1, len(reader.pages)):
    if(i % num_per_page == 0):
        # 一页已经满了，保存当前页
        merger.add_page(new_page)
        new_page = reader.pages[i]
        continue
    p1 = reader.pages[i]
    length = p1.cropbox.right
    height = p1.cropbox.top
    y_n = -int(i%num_per_page / num_per_row)
    x_n = i % num_per_row
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

# Write to an output PDF document
merger.add_page(new_page)
with open("package_output.pdf", "wb") as fp:
    merger.write(fp)