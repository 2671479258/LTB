# Generated by Django 3.2.23 on 2024-09-13 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureCity', models.CharField(max_length=20)),
                ('destinationCity', models.CharField(max_length=20)),
                ('departureDate', models.DateField()),
                ('start_time', models.CharField(max_length=20, null=True)),
                ('arrive_time', models.CharField(max_length=20, null=True)),
                ('start_place', models.CharField(max_length=20, null=True)),
                ('arrive_place', models.CharField(max_length=20, null=True)),
                ('price', models.CharField(max_length=20, null=True)),
            ],
            options={
                'verbose_name': '航班管理',
                'verbose_name_plural': '航班管理',
                'db_table': 'tb_flight',
            },
        ),
        migrations.CreateModel(
            name='Plane_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('logo', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': '航空公司管理',
                'verbose_name_plural': '航空公司管理',
                'db_table': 'plane_company',
            },
        ),
        migrations.CreateModel(
            name='Plane_Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plane.plane_company', verbose_name='所属公司')),
            ],
            options={
                'verbose_name': '飞机管理',
                'verbose_name_plural': '飞机管理',
                'db_table': 'plane_name',
            },
        ),
        migrations.CreateModel(
            name='Flight_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_name', models.CharField(max_length=100, verbose_name='乘客姓名')),
                ('passenger_gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=10, verbose_name='乘客性别')),
                ('passenger_phone', models.CharField(max_length=11, verbose_name='乘客手机号')),
                ('passenger_id', models.CharField(max_length=18, verbose_name='身份证号')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plane.flight', verbose_name='航班')),
            ],
            options={
                'verbose_name': '航班订单',
                'verbose_name_plural': '航班订单',
                'db_table': 'flight_order',
            },
        ),
    ]
