# BCG
Dependencies:
* Anaconda 2022.05 (10. Mai 2022)

Installation Guide (anaconda Prompt):
1) Create new virtual enviroment <br>
conda create --name runner_env python=3.9
2) Activate virtual enviroment <br>
conda activate runner_env
3) Install libraries <br>
pytorch: conda install pytorch torchvision pytorch-cuda=11.7 -c pytorch -c nvidia <br>
pynput: pip install pynput <br>
win32gui: pip install pywin32 <br>
sshkeyboard: pip install sshkeyboard <br>
4) Navigate to /temple_runner_steve/yolov5 and install requierements.txt <br>
pip install -r requirements.txt <br>
5) Navigate to /temple_runner_steve and open VScode <br>
code .

Training CNN (with single gpu): <br>
1) Navigate to /temple_runner_steve/yolov5 <br>
python train.py --img 320 --batch -1 --epochs 5 --data dataset.yml --weights yolov5s.pt --device 0

Training agent: <br>
1) Naviagte to /temple_runner_steve/ <br>
python agent.py <br>
