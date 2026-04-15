namespace py match_service

service Match{
	i32 add_player(1:i32 score,2:i32 id,3:i32 botId,4:string channel_name),

	i32 remove_player(1:i32 score,2:i32 id,3:i32 botId,4:string channel_name)
}