>scrapyd����scrapy��Ŀ

��װscrapyd��scrapyd-client
```shell
pip install scrapyd��
pip install scrapyd-client
```

����scrapy.cfg
```text
[settings]
default = job51.settings
 
[deploy:job51]#��������
url = http://localhost:6800/��#��Ŀ�������Ǹ���ַ
project = job51#��Ŀ����
```
������Ŀ,���������������
```shell script
scrapyd
```
�õ����½����

![image-20211220164606345](./scrapyd/scrapyd-deploy.png)

������Ŀ��

```shell
scrapyd-deploy job51 -p job51
```

![image-20211220164709618](C:\Users\����Դ\AppData\Roaming\Typora\typora-user-images\image-20211220164709618.png)

������ȣ�

![image-20211220164739799](C:\Users\����Դ\AppData\Roaming\Typora\typora-user-images\image-20211220164739799.png)

### ����SpiderKeeper

``` 
pip install spiderkeeper
```

����spiderkeeeper

```
spiderkeeeper
```

![image-20211220165048603](C:\Users\����Դ\AppData\Roaming\Typora\typora-user-images\image-20211220165048603.png)

��������� localhost:5000

```text
Ĭ���û�����admin
Ĭ�����룺admin
```

![image-20211220165215044](C:\Users\����Դ\AppData\Roaming\Typora\typora-user-images\image-20211220165215044.png)

