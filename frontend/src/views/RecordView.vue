<template>
    <ContentField>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <th>A</th>
                    <th>B</th>
                    <th>对战结果</th>
                    <th>对战时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="record in records" :key="record.id">
                    <td>
                        <img :src="record.a_photo" class="record-user-photo">
                        <span class="record-user-username">{{ record.a_username }}</span> 
                    </td>
                    <td>
                        <img :src="record.b_photo" class="record-user-photo">
                        <span class="record-user-username">{{ record.b_username }}</span>
                    </td>
                    <td>
                        {{ record.gameresult }}
                    </td>
                    <td>
                        {{ record.createTime }}
                    </td>
                    <td>
                        <button @click="open_record(record.id)" type="button" class="btn btn-secondary">查看录像</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <nav aria-label="...">
          <ul class="pagination" style="float:right">
            <li class="page-item" @click="click_page(-2)">
              <a class="page-link" href="#">Previous</a>
            </li>
            <li :class="'page-item '+page.is_active"
             v-for="page in pages" :key="page.number" 
             @click="click_page(page.number)">
                <a class="page-link" href="#">{{page.number}}</a>
            </li>
            <li class="page-item" @click="click_page(-1)">
              <a class="page-link" href="#">Next</a>
            </li>
          </ul>
        </nav>
    </ContentField>
</template>

<script type="text/javascript">
import ContentField from '../components/ContentField'
import $ from 'jquery'
import { ref } from 'vue'
import { useStore } from 'vuex'
import router from "../router/index"

export default{
    components:{
        ContentField
    },

    setup(){
        const store=useStore()
        let total_records=0
        let current_page=1
        let records=ref([])
        let pages=ref([])

        const click_page=page=>{
            if(page===-2)page=current_page-1;
            else if(page===-1)page=current_page+1;

            let max_pages=parseInt(Math.ceil(total_records/8));

            if(page>=1&&page<=max_pages){
                pull_pages(page)
            }
        }

        const update_pages=()=>{
            let max_pages=parseInt(Math.ceil(total_records/8));
            let new_pages=[];
            for(let i=current_page-2;i<=current_page+2;i++){
                if(i>=1&&i<=max_pages){
                    new_pages.push({
                        number:i,
                        is_active:i===current_page?"active":""
                    })
                }
            }
            pages.value=new_pages;
        }

        const pull_pages=(page)=>{
            current_page=page
            $.ajax({
                url:"https://snake.abiding.cn/api/getrecord/",
                type:"get",
                headers:{
                    Authorization:'Bearer '+store.state.user.token,
                },
                data:{
                    page:page
                },
                success(resp){
                    records.value=resp.data
                    total_records=resp.total_count;
                    update_pages()
                },
                error(resp){
                    console.log(resp)
                }
            })
        }
        pull_pages(current_page)
        const open_record=recordId=>{
            for(const record of records.value){
                if(record.id===recordId){
                    store.commit("updateIsRecord",true)
                    
                    store.commit("updateGame",{
                        map:record.gamemap,
                        a_id:record.a_id,
                        a_sx:record.a_sx,
                        a_sy:record.a_sy,
                        b_id:record.b_id,
                        b_sx:record.b_sx,
                        b_sy:record.b_sy,
                    })
                    console.log(store.state.pk.gamemap)
                    store.commit("updateSteps",{
                        a_steps:record.a_steps,
                        b_steps:record.b_steps
                    })

                    store.commit("updateRecordLoser",record.loser)
                    router.push({
                        name:"record_content_view",
                        params:{
                            recordId:recordId
                        }
                    })
                    break;
                }
            }
        }
        return{
            pages,
            records,
            open_record,
            update_pages,
            click_page
        }
    }
}
</script>

<style scoped>
img.record-user-photo{
    width: 5vh;
    border-radius: 50%;
}
</style>