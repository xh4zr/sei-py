# sei-py
A Caveon SEI helper library

```
import sei_py

client = sei_py.create_client_with_context(SEI_ID, SEI_SECRET, SEI_EXAM_ID, SEI_ROLE_SECRET)

exam = client.exam.get()

delivery = client.delivery.get(<delivery_id>, \
        include='''examinee,score_token,cached_exam_settings,form,
        accommodations,logs,item_responses,change_logs,exam''')
```
