<template>
    <div class="container">
        <div class="row">
            <div class="col-3">
                <div class="card" style="margin-top: 20px;">
                    <div class="card-body">
                        <img :src="$store.state.user.photo" alt="" style="width:100%;">
                    </div>
                </div>
            </div>
            <div class="col-9">
                <div class="card" style="margin-top: 20px;">
                    <div class="card-header">
                        <span style="font-size: 130%;">我的Bot</span>
                        <button type="button" class="btn btn-primary float-end" data-bs-toggle="modal" data-bs-target="#add-bot-btn">创建Bot</button>
                    </div>

                    <!-- Modal -->
                    <div class="modal fade" id="add-bot-btn" tabindex="-1" >
                      <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">创建Bot</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <div class="mb-3">
                              <label for="bot-add-title" class="form-label">名称</label>
                              <input v-model="bot_add.title" type="text" class="form-control" id="bot-add-title" placeholder="请输入Bot名称">
                            </div>
                            <div class="mb-3">
                              <label for="bot-add-description" class="form-label">简介</label>
                              <textarea v-model="bot_add.description" class="form-control" id="bot-add-description" rows="2" placeholder="请输入Bot简介"></textarea>
                            </div>
                            <div class="mb-3">
                              <label for="bot-add-code" class="form-label">代码</label>
                              <!-- <textarea v-model="bot_add.content" class="form-control" id="bot-add-code" rows="5" placeholder="请输入Bot代码"></textarea> -->
                              <VAceEditor
                                v-model:value="bot_add.content"
                                @init="editorInit"
                                lang="c_cpp"
                                theme="textmate"
                                style="height: 300px" />
                            </div>

                          </div>
                          <div class="modal-footer">
                            <div class="error-message">{{ bot_add.error_message }}</div>
                            <button type="button" class="btn btn-primary" @click="add_bot">创建</button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="card-body">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>名称</th>
                                    <th>创建时间</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="bot in bots" :key="bot.id">
                                    <td>{{ bot.title }}</td>
                                    <td>{{ bot.createTime }}</td>
                                    <td>
                                        <button type="button" class="btn btn-secondary" style="margin-right: 10px;" data-bs-toggle="modal" :data-bs-target="'#update-bot-btn-'+bot.id">修改</button>
                                        <button type="button" class="btn btn-danger" @click="remove_bot(bot)">删除</button>
                                        <!-- Modal -->
                                        <div class="modal fade" :id="'update-bot-btn-'+bot.id" tabindex="-1" >
                                          <div class="modal-dialog modal-xl">
                                            <div class="modal-content">
                                              <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel">修改Bot</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                              </div>
                                              <div class="modal-body">
                                                <div class="mb-3">
                                                  <label for="bot-add-title" class="form-label">名称</label>
                                                  <input v-model="bot.title" type="text" class="form-control" id="bot-add-title" placeholder="请输入Bot名称">
                                                </div>
                                                <div class="mb-3">
                                                  <label for="bot-add-description" class="form-label">简介</label>
                                                  <textarea v-model="bot.description" class="form-control" id="bot-add-description" rows="2" placeholder="请输入Bot简介"></textarea>
                                                </div>
                                                <div class="mb-3">
                                                  <label for="bot-add-code" class="form-label">代码</label>
                                                  <!-- <textarea v-model="bot.content" class="form-control" id="bot-add-code" rows="5" placeholder="请输入Bot代码"></textarea> -->
                                                  <VAceEditor
                                                    v-model:value="bot.content"
                                                    @init="editorInit"
                                                    lang="c_cpp"
                                                    theme="textmate"
                                                    style="height: 300px" />
                                                </div>

                                              </div>
                                              <div class="modal-footer">
                                                <div class="error-message">{{ bot.error_message }}</div>
                                                <button type="button" class="btn btn-primary" @click="update_bot(bot)">保存修改</button>
                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                              </div>
                                            </div>
                                          </div>
                                        </div>

                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
import $ from 'jquery'
import { useStore } from 'vuex'
import { ref,reactive } from 'vue'
import { Modal } from 'bootstrap/dist/js/bootstrap'
import { VAceEditor } from 'vue3-ace-editor'
import ace from 'ace-builds'

export default{
    components:{
        VAceEditor,
    },
    setup(){
        ace.config.set(
    "basePath", 
    "https://cdn.jsdelivr.net/npm/ace-builds@" + require('ace-builds').version + "/src-noconflict/")
        const store=useStore()
        let bots=ref([])
        let bot_add=reactive({
            title:"",
            description:"",
            content:"",
            error_message:""
        })

        const refresh_bots=()=>{
            $.ajax({
              url:"https://snake.abiding.cn/api/bot/list/",
              type:"get",
              headers:{
                'Authorization':"Bearer "+store.state.user.token,
              },
              success(resp){
                console.log(resp)
                bots.value=resp.bots
              },
              error(resp){
                console.log(resp)
              }
            })
        }
        refresh_bots()

        const add_bot=()=>{
            bot_add.error_message="";
            $.ajax({
                url:"https://snake.abiding.cn/api/bot/add/",
                type:"post",
                data:{
                    title:bot_add.title,
                    description:bot_add.description,
                    content:bot_add.content
                },
                headers:{
                    Authorization:'Bearer '+store.state.user.token
                },
                success(resp){
                    if(resp.result==="success"){
                        bot_add.title="";
                        bot_add.description=""
                        bot_add.content=""
                        Modal.getInstance("#add-bot-btn").hide()
                        refresh_bots()
                    }else{
                        bot_add.error_message=resp.result
                    }
                }
            })
        }
        const remove_bot=(bot)=>{
            $.ajax({
              url:"https://snake.abiding.cn/api/bot/remove/",
              type:"post",
              data:{
                bot_id:bot.id
              },
              headers:{
                'Authorization':"Bearer "+store.state.user.token,
              },
              success(resp){
                if(resp.result==="success"){
                    refresh_bots()
                }
              },
              error(resp){
                console.log(resp)
              }
            })
        }
        const update_bot=(bot)=>{
            bot_add.error_message="";
            $.ajax({
                url:"https://snake.abiding.cn/api/bot/update/",
                type:"post",
                data:{
                    bot_id:bot.id,
                    title:bot.title,
                    description:bot.description,
                    content:bot.content
                },
                headers:{
                    Authorization:'Bearer '+store.state.user.token
                },
                success(resp){
                    if(resp.result==="success"){
                        Modal.getInstance('#update-bot-btn-'+bot.id).hide()
                        refresh_bots()
                    }else{
                        bot.error_message=resp.result
                    }
                }
            })
        }
        return {
            bots,
            bot_add,
            add_bot,
            update_bot,
            remove_bot
        }
        
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/update/",
        //   type:"post",
        //   data:{
        //     bot_id:1,
        //     title:"dfsfsf",
        //     description:"fffffffffff",
        //     content:"tsfeef",
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/remove/",
        //   type:"post",
        //   data:{
        //     bot_id:5
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/add/",
        //   type:"post",
        //   data:{
        //     title:"123",
        //     description:"",
        //     content:"test",
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
    }
}
</script>

<style scoped>
.container{
    width: 70%;
}
.error-message{
    color: red;
}
</style>