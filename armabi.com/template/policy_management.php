<div class="managements">
    <div class="window-grid" id="policyM">
        <div class="obl-1"><p>Управление политиками</p></div>
        <div class="obl-2"><img  src="images/Icons/delete2.png" width="25" height="25" style="float:right;" onclick="modalWindowDisable('p-m','all-f')"></img></div>
        <div class="obl-3">
            <div class="tree-catalog">
                <div class="demo frmt" ></div>
			</div>
        </div>
        <div class="obl-4">
            
            <b-tabs fill small class="aud-res-p-m" style="height:100%;width:100%">
                <b-tab title="Дискретационные атрибуты"  :active="isActiveDiscrete">
                        <table style="width:100%;white-space:nowrap" >
                            <tr>
                                <th style="width:50%;">
                                    <label>Пользователи</label><br>
                                    <b-form-select v-model="discrete_users" :options="get_discrete_users" text-field="text" value-field="text"  size="sm" style="width: 250px">
                                        <template #first>
                                            <b-form-select-option value="null" disabled>--Локальные пользователи--</b-form-select-option>
                                        </template>
                                    </b-form-select><br>
                                    
                                
                                    <label>Группы</label><br>
                                    <b-form-select v-model="discrete_groups" :options="get_discrete_groups" text-field="text" value-field="text" size="sm" style="width: 250px">
                                            <template #first>
                                                <b-form-select-option value="null" disabled>--Локальные группы--</b-form-select-option>
                                            </template>
                                    </b-form-select>
                                </th>
                                <th>
                                    <b-form-checkbox
                                    v-for="option in all_discrete_bit_arr"
                                    v-model="get_discrete_bit"
                                    :key="option.text"
                                    :value="option.text"
                                    size="lg" 
                                    class="mb-3"
                                    plain>
                                        {{ option.text }}
                                    </b-form-checkbox>
                                </th>
                            </tr>
                            
                            <tr>
                                <td colspan="2">
                                    <label>Владелец</label><br>
                                    <b-form-group
                                    v-slot="{ ariaDescribedby }">
                                        <b-form-checkbox
                                        v-for="option in all_discrete_dostup"
                                        v-model="get_owner"
                                        :key="option.text"
                                        :value="option.text"
                                        :aria-describedby="ariaDescribedby"
                                        name="flavour-3a" 
                                        plain
                                        inline>
                                            {{ option.text }}
                                        </b-form-checkbox>
                                    </b-form-group>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <label>Группа</label><br>
                                    <b-form-group
                                    v-slot="{ ariaDescribedby }">
                                        <b-form-checkbox
                                        v-for="option in all_discrete_dostup"
                                        v-model="get_group"
                                        :key="option.text"
                                        :value="option.text"
                                        :aria-describedby="ariaDescribedby"
                                        name="flavour-3a" 
                                        plain
                                        inline>
                                            {{ option.text }}
                                        </b-form-checkbox>
                                    </b-form-group>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <label>Остальные</label><br>
                                    <b-form-group
                                    v-slot="{ ariaDescribedby }">
                                        <b-form-checkbox
                                        v-for="option in all_discrete_dostup"
                                        v-model="get_other"
                                        :key="option.text"
                                        :value="option.text"
                                        :aria-describedby="ariaDescribedby"
                                        name="flavour-3a" 
                                        plain
                                        inline>
                                            {{ option.text }}
                                        </b-form-checkbox>
                                    </b-form-group>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <b-form-checkbox value="1" v-model="install_recursiv" plain>Рекурсивно</b-form-checkbox>
                                </td>
                                <td style="text-align:right">
                                    <button>Применить</button>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <label>Правила ACL</label><br>
                                    <label>Тип субъекта</label><br>
                                    <b-form-select v-model="get_acl_subject" :options="all_acl_subject" text-field="text" value-field="text" size="sm" @change="checkSubiectActive"></b-form-select>
                                    
                                </td>
                                <td>
                                    <label v-show="d_acl_sub_show">Cубъект</label><br>
                                    <b-form-checkbox value="true" v-model="d_acl_check_sub" plain v-show="d_acl_sub_show" @change="checkSubiectActive">
                                        <b-form-select
                                        v-model="default_acl_sub_user" 
                                        :options="get_acl_sub_user" 
                                        text-field="text" 
                                        value-field="text" 
                                        size="sm" 
                                        v-show="d_acl_sub_show" 
                                        :disabled="d_acl_sub_disable">
                                            <template #first>
                                                <b-form-select-option value="null" disabled>--Локальные пользователи--</b-form-select-option>
                                            </template>
                                        </b-form-select>
                                    </b-form-checkbox>
                                </td>
                            </tr>
                            
                            <tr>
                                <td>
                                    <b-form-group
                                    v-slot="{ ariaDescribedby }">
                                        <b-form-checkbox
                                        v-for="option in acl_dostup"
                                        v-model="get_acl_dostup"
                                        :key="option.text"
                                        :value="option.text"
                                        :aria-describedby="ariaDescribedby"
                                        name="flavour-3a" 
                                        plain
                                        inline>
                                            {{ option.text }}
                                        </b-form-checkbox>
                                    </b-form-group>
                                </td>
                                <td>
                                    
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <b-form-checkbox value="1" v-model="d_acl_recursiv" plain text-field="text" value-field="text">Рекурсивно</b-form-checkbox>
                                </td>
                                <td style="text-align:right">
                                   <button>Добавить/Изменить</button> 
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <b-table striped hover responsive="sm" 
                                    :items="get_acl_table" 
                                    selectable 
                                    :select-mode="selectMode"
                                    outlined
                                    :head-row-variant="headVariant"
                                    sticky-header="20vh">
                                                                            
                                        <template #cell(delAccess)="data">
                                            <span v-html="data.value"></span>
                                        </template>
                                            
                                    </b-table>
                                </td>
                            </tr>
                        </table>
                    
                    
                </b-tab>
                
                <b-tab title="Аудит реусурсов" :active="isActiveAudit">
                    <table style="width:100%;white-space:nowrap">
                        <tr>
                            <th style="width:50%">
                                <label>Тип субъекта</label><br>
                                <b-form-select v-model="audit_visible" :options="audit_type_sub" text-field="text" value-field="text" size="sm">
                                </b-form-select>
                            </th>
                            <th style="width:50%">
                                <label>Cубъект</label><br>
                                <b-form-select v-model="audit_visible_user" :options="audit_user_sub" text-field="text" value-field="text" size="sm">
                                    <template #first>
                                    <b-form-select-option value="null" disabled>--Локальные пользователи--</b-form-select-option>
                                    </template>
                                </b-form-select>
                            </th>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <b-form-group v-slot="{ ariaDescribedby }">
                                    Успех
                                    <b-form-checkbox
                                    v-for="option in all_properties"
                                    v-model="marked_audit_yes"
                                    :key="option.text"
                                    :value="option.text"
                                    :aria-describedby="ariaDescribedby"
                                    name="flavour-3a" 
                                    plain
                                    inline
                                    @change=selectionAllOptionsYes>
                                        {{ option.text }}
                                    </b-form-checkbox>
                                </b-form-group>
                
                    
                                <b-form-group v-slot="{ ariaDescribedby }">
                                    Неудача
                                    <b-form-checkbox
                                    v-for="option in all_properties"
                                    v-model="marked_audit_no"
                                    :key="option.text"
                                    :value="option.text"
                                    :aria-describedby="ariaDescribedby"
                                    name="flavour-3a" 
                                    plain
                                    inline
                                    @change=selectionAllOptionsNo>
                                        {{ option.text }}
                                    </b-form-checkbox>
                                </b-form-group>
                            </td>
                        </tr>
                    </table>
                    
                </b-tab>
                <b-tab title="Мандатные атрибуты" :active="isActiveMandate">
                    
                </b-tab>
            </b-tabs>
            
        </div>
    </div>
    
</div>
