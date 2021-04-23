import json 


def read_json(json_path):

    with open(json_path, 'r') as f:
        json_file = json.load(f)
    return json_file

def save_json(json_path, json_file):
    with open(json_path, 'w') as f:
        json.dump(json_file, f, indent=1)

if __name__ == '__main__':

    json_path_1 = '/home/xiaozhiheng/Downloads/instances_val1.json'
    json_path_2 = '/home/xiaozhiheng/Downloads/instances_val2(1).json'
    save_path = '/home/xiaozhiheng/Downloads/instances.json'
    json_file_1 = read_json(json_path_1)
    json_file_2 = read_json(json_path_2)
    
    if len(json_file_1['images']) > len(json_file_2['images']):
        json_file_1, json_file_2 = json_file_2, json_file_1

    length_1 = len(json_file_1['images'])
    image_list_1 = json_file_1['images']
    annotation_list_1 = json_file_1['annotations']
    cate_list_1 = json_file_1['categories']

    length_2 = len(json_file_2['images'])
    image_list_2 = json_file_2['images']
    annotation_list_2 = json_file_2['annotations']
    cate_list_2 = json_file_2['categories']
    len_ann_2 = len(annotation_list_2)
    name_list_1 = [item['name'] for item in cate_list_1]
    name_list_2 = [item['name'] for item in cate_list_2]
    name_list_1.extend(name_list_2)
    name_list = sorted(set(name_list_1))
    cate_list = []
    for i, name in enumerate(name_list):
        cate_list.append({
            'id':i,
            'name': name,
            'supercategory': name
        })
    # print(cate_list)

    map_1 = {item['id']: item['name'] for item in cate_list_1}
    map_2 = {item['id']: item['name'] for item in cate_list_2}
    map_new = {item['name']:item['id'] for item in cate_list}

    # 修改对应的 category_id
    for annotation_2 in annotation_list_2:
        category_id = annotation_2['category_id']
        category_name = map_2[category_id]
        new_category_id = map_new[category_name]
        annotation_2['category_id'] = new_category_id

    #修改id
    for image_1 in image_list_1:
        image_1['id'] = image_1['id'] + length_2
        image_list_2.append(image_1)

    for annotation_1 in annotation_list_1:

        category_id = annotation_1['category_id']
        category_name = map_1[category_id]
        new_category_id = map_new[category_name]
        annotation_1['category_id'] = new_category_id

        annotation_1['image_id'] = annotation_1['image_id'] + length_2

        annotation_1['id'] = annotation_1['id'] + len_ann_2
        annotation_list_2.append(annotation_1)

    image_list = image_list_2
    annotation_list = annotation_list_2 
    
    json_file = {
        'images':image_list,
        'categories':cate_list,
        'annotations': annotation_list
    }

    save_json(save_path, json_file)

    


    print('done')
    # print(set(img_id))

