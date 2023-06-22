<b-table striped hover responsive="sm" 
    :items="devices"
    :fields="devices_name"
    selectable 
    :select-mode="selectMode"
    outlined
    :head-row-variant="headVariant"
    @row-selected="onRowSelected" >
                                    
    <template #cell(Имя_хоста_(ip_и_mac_адрес))="data">
        <span v-html="data.value"></span>
    </template>
    <template #cell(Регистрация)="data">
        <span v-html="data.value"></span>
    </template>
    <template #cell(Контр.домена)="data">
        <span v-html="data.value"></span>
    </template>
    <template #cell(Активность_хоста)="data">
        <span v-html="data.value"></span>
    </template>
    <template #cell(Активность_агента)="data">
        <span v-html="data.value"></span>
    </template>
</b-table>
  
 
