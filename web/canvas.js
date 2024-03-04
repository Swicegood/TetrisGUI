var canvas = document.querySelector('canvas');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;






var c = canvas.getContext('2d');

//buffer canvas

//var canvas2 = document.getElementById('canvas2');
//if(canvas2){
//canvas2.width = window.innerWidth;
//canvas2.height = window.innerHeight;
//}
//var d = canvas2.getContext('2d');


let my_websocket_addr = (eel._host + '/eel').replace('http', 'ws');
            websocket2 = new WebSocket(my_websocket_addr);


document.addEventListener('keydown', function(event) {
    websocket2.send(event.keyCode)
    });


eel.expose(clear_canvas_js);
function clear_canvas_js(){
    c.clearRect(0, 0, canvas.width, canvas.height);

    }

eel.expose(draw_text_js);
function draw_text_js(line,x,y){
    c.font = "30px Monospace";
    c.fillText(line, x, y);

    }


var block_blue = new Image();
block_blue.src = "block_blue.png";

var block_gold = new Image();
block_gold.src = "block_gold.png";

var block_purple = new Image();
block_purple.src = "block_purple.png";

var block_darkblue = new Image();
block_darkblue.src = "block_darkblue.png";

var block_yellow = new Image();
block_yellow.src = "block_yellow.png";

var block_red = new Image();
block_red.src = "block_red.png";

var block_green = new Image();
block_green.src = "block_green.png";




eel.expose(draw_rect_js);
function draw_rect_js(x,y,char){
   switch(char){
       case '|':
       c.fillStyle = "#000000";
       c.fillRect((x*16),(y*16),16,16);
       break;
       case 'A':
       c.drawImage(block_blue,x*16,y*16);
       break;
       case 'B':
       c.drawImage(block_gold,x*16,y*16);
       break;
       case 'C':
       c.drawImage(block_purple,x*16,y*16);
       break;
       case 'D':
        c.drawImage(block_darkblue,x*16,y*16);
       break;
       case 'E':
        c.drawImage(block_red,x*16,y*16);
       break;
       case 'F':
        c.drawImage(block_yellow,x*16,y*16);
       break;
       case 'G':
       c.drawImage(block_green,x*16,y*16);
       break;
       case ' ':
       c.fillStyle = "#FFFFFF";
       c.fillRect((x*16),(y*16),16,16);
       break;
   }

}

eel.expose(print_js);
function print_js(board){
    for (i =0; i < board.length; i++){
         for (j = 0; j < 12; j++){
             draw_rect_js(j,i,board[i][j]);

        }
    }
}

