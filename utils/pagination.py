# -*- coding:utf-8 -*-

class Page(object):

    def __init__(self,current_page,data_count,per_page_count=10, page_num=7):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = page_num
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return (self.current_page ) * self.per_page_count

    @property    #下面调用的时候不想加括号，
    def all_count(self):
        v,y = divmod(self.data_count,self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self,base_url):
        page_list = []
        # 控制页码显示
        page_num = 7
        if self.all_count < page_num:
            start_index = 1
            end_index = self.all_count + 1
        else:
            if self.current_page <= (page_num + 1) / 2:
                start_index = 1
                end_index = page_num + 1
            else:
                start_index = self.current_page - (page_num - 1) / 2
                end_index = self.current_page + (page_num + 1) / 2
                if self.current_page + (page_num - 1) / 2 > self.all_count:
                    end_index = self.all_count + 1
                    start_index = self.all_count - (page_num - 1)

        if self.current_page == 1:
            prev = '<li><a class= "page" href="javascript:void(0);">上一页</a></li>'
            page_list.append(prev)
        else:
            prev = '<li><a class= "page" href="%s?p=%s">上一页</a></li>' % (base_url,self.current_page - 1)
            page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:  # .pagination .page.active   page和active没有空格
                temp = '<li><a class= "page active" href="%s?p=%s">%s</a></li>' % (base_url,i, i)
            else:  # 根据选中的页面，显示不同样式
                temp = '<li><a class= "page" href="%s?p=%s">%s</a></li>' % (base_url,i, i)
            page_list.append(temp)

        if self.current_page == self.all_count:
            prev = '<li><a class= "page" href="javascript:void(0);">下一页</a></li>'
            page_list.append(prev)
        else:
            prev = '<li><a class= "page" href="%s?p=%s">下一页</a></li>' % (base_url,self.current_page + 1)
            page_list.append(prev)
        #
        # jump = '''
        #    <input type = 'text'><a onclick="jumpTo(this,'%s?p=');">GO</a>
        #    <script>
        #        function jumpTo(ths,base){
        #            var val = ths.previousSibling.value;
        #            location.href = base + val;
        #        }
        #    </script>
        #    '''%(base_url)
        # page_list.append(jump)
        page_str = ''.join(page_list)  # 4.将列表转成总字符串'<a href="/user_list/?p=%s">%s</a>
        from django.utils.safestring import mark_safe
        page_str = mark_safe(page_str)  # 将插入html中的字符串变成安全代码，可以被解释
        # 默认页面的所有变量都会被转义，防止xss攻击
        return page_str
