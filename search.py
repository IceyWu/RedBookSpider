import json
import re
import requests
from one import OneNote
from xhs_utils.xhs_util import get_headers, get_search_data, get_params, js
from tqdm import tqdm

class Search:
    def __init__(self):
        self.search_url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
        self.headers = get_headers()
        self.params = get_params()
        self.oneNote = OneNote()
        self.cookies = self.oneNote.cookies

    def get_search_note(self, query, number):
        data = get_search_data()
        api = '/api/sns/web/v1/search/notes'
        data = json.dumps(data, separators=(',', ':'))
        data = re.sub(r'"keyword":".*?"', f'"keyword":"{query}"', data)
        page = 0
        note_ids = []
        while len(note_ids) < number:
            page += 1
            data = re.sub(r'"page":".*?"', f'"page":"{page}"', data)
            ret = js.call('get_xs', api, data, self.cookies['a1'])
            self.headers['x-s'], self.headers['x-t'] = ret['X-s'], str(ret['X-t'])
            response = requests.post(self.search_url, headers=self.headers, cookies=self.cookies, data=data.encode('utf-8'))
            res = response.json()
            if not res['data']['has_more']:
                print(f'搜索结果数量为 {len(note_ids)}, 不足 {number}')
                break
            items = res['data']['items']
            for note in items:
                note_id = note['id']
                note_ids.append(note_id)
                if len(note_ids) >= number:
                    break
        return note_ids

    def handle_note_info(self, query, number, sort, note_type, need_cover=False):
        data = get_search_data()
        data['sort'] = sort
        data['note_type'] = note_type
        api = '/api/sns/web/v1/search/notes'
        data = json.dumps(data, separators=(',', ':'))
        data = re.sub(r'"keyword":".*?"', f'"keyword":"{query}"', data)
        page = 0
        index = 0
        while index < number:
            page += 1
            data = re.sub(r'"page":".*?"', f'"page":"{page}"', data)
            ret = js.call('get_xs', api, data, self.cookies['a1'])
            self.headers['x-s'], self.headers['x-t'] = ret['X-s'], str(ret['X-t'])
            response = requests.post(self.search_url, headers=self.headers, cookies=self.cookies, data=data.encode('utf-8'))
            res = response.json()
            if not res['data']['has_more']:
                print(f'搜索结果数量为 {index}, 不足 {number}')
                break
            items = res['data']['items']
            for note in items:
                index += 1
                self.oneNote.save_one_note_info(self.oneNote.detail_url + note['id'], need_cover, '', 'datas_search',query)

                if index >= number:
                    break

            # 使用tqdm优化进度条
            # for note in tqdm(items, desc='搜索结果下载进度'):
            #     index += 1
            #     self.oneNote.save_one_note_info(self.oneNote.detail_url + note['id'], need_cover, '', 'datas_search',query)

            #     if index >= number:
            #         break

        print(f'搜索结果全部下载完成，共 {index} 个笔记')


    def main(self, query, number, sort, note_type):
        self.handle_note_info(query, number, sort, note_type, need_cover=True)


if __name__ == '__main__':
    search = Search()
    # 搜索的关键词
    query = '平潭岛'
    # 搜索的数量（前多少个）
    number = 2
    # 排序方式 general: 综合排序 popularity_descending: 热门排序 time_descending: 最新排序
    sort = 'general'
    # 笔记类型 0: 全部 1:视频  2:图片 
    note_type = 0
    search.main(query, number, sort, note_type)
