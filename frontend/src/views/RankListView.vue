<template>
    <ContentField>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <th>玩家</th>
                    <th>分数</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>
                        <img :src="user.photo" class="record-user-photo">
                        <span class="record-user-username">{{ user.username }}</span> 
                    </td>
                    <td>
                        {{ user.score }}
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

export default{
    components:{
        ContentField
    },

    setup(){
        const store=useStore()
        let total_users=0
        let current_page=2
        let users=ref([])
        let pages=ref([])

        const click_page=page=>{
            if(page===-2)page=current_page-1;
            else if(page===-1)page=current_page+1;

            let max_pages=parseInt(Math.ceil(total_users/8));

            if(page>=1&&page<=max_pages){
                pull_pages(page)
            }
        }

        const update_pages=()=>{
            let max_pages=parseInt(Math.ceil(total_users/8));
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
                url:"https://snake.abiding.cn/api/ranklist/",
                type:"get",
                headers:{
                    Authorization:'Bearer '+store.state.user.token,
                },
                data:{
                    page:page
                },
                success(resp){
                    users.value=resp.data
                    total_users=resp.total_count;
                    update_pages()
                    console.log(resp)
                },
                error(resp){
                    console.log(resp)
                }
            })
        }
        pull_pages(current_page)
        
        return{
            pages,
            users,
            click_page,

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