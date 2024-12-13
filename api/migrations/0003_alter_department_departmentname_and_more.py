# Generated by Django 5.1.4 on 2024-12-13 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_department_salaryhistory_jobposition_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='departmentName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dni',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='employee',
            name='firstName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='lastName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phoneNumber',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='jobposition',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobposition',
            name='jobPositionName',
            field=models.CharField(max_length=255),
        ),
    ]
