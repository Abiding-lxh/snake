const SNAKE_GAME_OBJECTS=[]

export class SnakeGameObject{
	constructor(){
		SNAKE_GAME_OBJECTS.push(this);

		this.timedelta=0;
		this.has_called_start=false;
	}
	start(){
	}
	update(){
	}
	on_destroy(){
	}
	destroy(){
		this.on_destroy();
		for(let i in SNAKE_GAME_OBJECTS){
			const obj = SNAKE_GAME_OBJECTS[i];
			if(obj===this){
				SNAKE_GAME_OBJECTS.splice(i,1);
				break;
			}
		}
	}
}
let last_timestamp;

const step= timestamp =>{
	for(let obj of SNAKE_GAME_OBJECTS){
		if(!obj.has_called_start){
			obj.has_called_start=true;
			obj.start();
		}else{
			obj.timedelta=timestamp-last_timestamp;
			obj.update();
		}
	}
	last_timestamp=timestamp;
	requestAnimationFrame(step)
}

requestAnimationFrame(step);