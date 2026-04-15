namespace py bot_run_service

service BotRun{
	i32 add_bot(1:i32 id,2:i32 botId,3:string bot_code,4:string input,5:string channel_name)
}