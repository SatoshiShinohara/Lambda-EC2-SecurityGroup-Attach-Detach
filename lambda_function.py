import logging
import boto3

def lambda_handler(event, context):
    target_instance_ids=['i-XXXXXXXXXXXXXXXXX',
                         'i-YYYYYYYYYYYYYYYYY',
                         'i-XXXXXXXXXXXXXXXXX']  # 対象インスタンス
    append_remove_sg_id='sg-00000000000000000'   # アタッチ・デタッチするセキュリティグループ

    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(InstanceIds=target_instance_ids)

    # インスタンス分ループ
    for instance in instances:
        # インスタンスにアタッチされているセキュリティグループを取得
        all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]

        if event['action'] == 'attach':
            if append_remove_sg_id not in all_sg_ids:  # 追加対象のセキュリティグループが既にインスタンスにアタッチされていない場合のみアタッチする
                all_sg_ids.append(append_remove_sg_id)
                instance.modify_attribute(Groups=all_sg_ids)
            else:
                logging.warning(append_remove_sg_id + ' is already attached to ' + instance.id)

        elif event['action'] == 'detach':
            if append_remove_sg_id in all_sg_ids:  # 削除対象のセキュリティグループが既にインスタンスからデタッチされていない場合のみデタッチする
                all_sg_ids.remove(append_remove_sg_id)
                instance.modify_attribute(Groups=all_sg_ids)
            else:
                logging.warning(append_remove_sg_id + ' is already detached to ' + instance.id)
