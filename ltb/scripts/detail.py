# 添加 django 环境
import os, sys
import django

# 1. 找到当前项目的上一级目录
from django.db.models import Min
sys.path.insert(0, '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ltb.settings')
django.setup()
from users.models import Hotel, Roomtype
def generic_detail_html(hotel):
    roomtypes = Roomtype.objects.filter(hotel=hotel)
    min_price = roomtypes.aggregate(Min('price'))['price__min']
    context = {
        'hotel': hotel,
        'roomtypes': roomtypes,  # 将房间数据添加到上下文
        'min_price': min_price,  # 最小房间价格
    }
    from django.template import loader
    detail_template = loader.get_template('detail.html')
    detail_html_data = detail_template.render(context)
    # 3. 写入文件
    import os
    from ltb import settings
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front/hotels/%s.html' % hotel.id)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(detail_html_data)
        print(hotel.id)
hotels = Hotel.objects.all()
for hotel in hotels:
    generic_detail_html(hotel)

