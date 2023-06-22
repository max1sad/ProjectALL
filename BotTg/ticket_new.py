import DBProvide
import action_file
import logger
def ticket():
    last_id = action_file.file_read()
    new_id = DBProvide.get_max_id_ticket()[0][0]
    if last_id:
        action_file.file_write(str(new_id))
        return new_ticket(last_id)
    else:  
        if new_id:
            action_file.file_write(str(new_id))
        else:
            logger.file_log("В таблице ticket нет записей !!!")
        return 0
    
def new_ticket(max_id):
    group_ticket = DBProvide.get_new_ticket_in_group(max_id)
    if group_ticket:
        return group_ticket
    else:
        return 0




