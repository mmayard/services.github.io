// P_3_0_01
//

/**
 * changing the size and the position of a letter
 *
 * MOUSE
 * position x          : size
 * position y          : position
 * drag                : draw
 *
 * KEYS
 * a-z                 : change letter
 * ctrl                : save png
 */
'use strict';

var font = 'sans-serif';
var letter = 'M—S™';

function setup() {
  createCanvas(windowWidth, windowHeight);
  fill(255);

  textFont(font);
  textAlign(CENTER, CENTER);
  blendMode(DIFFERENCE);
}

function mouseMoved() {
  clear();
  textSize((mouseX - width / 2) * 5 + 1);
  text(letter, width / 2, mouseY);
}

function mouseDragged() {
  textSize((mouseX - width / 2) * 5 + 1);
  text(letter, width / 2, mouseY);
}

function keyReleased() {
  if (keyCode == CONTROL) saveCanvas(gd.timestamp(), 'png');
}

function keyTyped() {
  letter = key;
}
