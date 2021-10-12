
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts
import os

RED = '\x1b[1;91m'
BLUE = '\033[1;94m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
ENDC = '\033[0m'

def title():
    print(RED + '''
    Title: kite-文档PDF批量根据文件名添加水印
    Version: V1.0.0
    ''' + ENDC)

# 创建水印信息
def create_watermark(content,watername):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    file_name = watername
    # 水印PDF页面大小
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(4 * cm, 0 * cm)
    # 设置字体格式与大小,中文需要加载能够显示中文的字体，否则就会乱码，注意字体路径
    try:
        reportlab.pdfbase.pdfmetrics.registerFont(
            reportlab.pdfbase.ttfonts.TTFont('yahei', 'C:\\Windows\\Fonts\\STKAITI.TTF'))
        c.setFont('yahei', 50)
    except:
        # 默认字体，只能够显示英文
        c.setFont("Helvetica", 30)
        content = "watermark"

    # 旋转角度度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0)
    # 设置透明度,1为不透明
    c.setFillAlpha(0.05)
    # 画几个文本,注意坐标系旋转的影响
    c.drawString(0 * cm, 3 * cm, content)
    # 关闭并保存pdf文件
    c.save()
    return file_name


# 插入水印
def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    pdf_output = PdfFileWriter()
    input_stream = open('./files/'+ pdf_file_in, 'rb')
    pdf_input = PdfFileReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pageNum = pdf_input.getNumPages()

    # 读入水印pdf文件
    pdf_watermark = PdfFileReader(open(pdf_file_mark, 'rb'), strict=False)
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        page.mergePage(pdf_watermark.getPage(0))
        page.compressContentStreams()  # 压缩内容
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


if __name__ == '__main__':
    title()
    # pdf_file_in = 'watermark1.pdf'
    # pdf_file_out = 'watermark.pdf'
    print( BLUE + '请将你需要添加文件的水印放在files文件夹里面' + ENDC)
    print( BLUE + '运行后会在当前目录下生成，水印跟文件名一样，若需要修改请联系开发者或者自己改' + ENDC)
    print( BLUE + '水印信息在第21行，请根据自己需求修改字体、大小等' + ENDC)
    print(input(GREEN + '一切准备好的话，请按任意键继续' +ENDC))
    # 批量读取文件名-水印文件-mark
    file_path = "./files/" # 目标文件放在./files目录下
    filenames_mark = os.listdir(file_path)
    for i in range(len(filenames_mark)):
        pdf_file_mark = create_watermark(filenames_mark[i],'water'+filenames_mark[i])
        # 批量读取文件名-原有需要插入的PDF
        pdf_file_in = filenames_mark[i]
        ## 接下来是在原有的pdf插入水印
        pdf_file_out = filenames_mark[i]  # 这里是要输出的文件名
        add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out)


