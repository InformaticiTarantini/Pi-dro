__author__ = 'walter'
from webserver import app
from flask import render_template, request, url_for
from robot import Robot
import json
import logging


log = logging.getLogger(app.config.get('LOGGER_NAME'))
robot = Robot()
actions = {"stop": robot.standby,
           "forward": robot.move_forward,
           "backward": robot.move_backward,
           "left": robot.move_left,
           "right": robot.move_right}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/action/<action>', methods=["GET", "POST"])
def do_action(action):
    move = actions.get(action)
    if not move:
        return json.dumps({'error': 'Wrong action'})
    move()
    return json.dumps({'result': 'Move done'})


def main():
    app.run(port=app.config.get("PORT"), host=app.config.get("HOST"))
    robot.off()

if __name__ == '__main__':
    main()