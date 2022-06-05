# Evolution Project
Evolution simulation written in Python3
## Description
The project reflects the simplest evolutionary processes and predator-prey relations. In our implementation, there are two species: the first one receives energy from sunlight during photosynthesis, and the second one hunts for the first. There are certain rules by which organisms are guided: if the energy level is lower than a specific number, an organism stops moving or dies if it is lower than zero, otherwise, it is constantly moving (up, right, left or right). The direction is embedded in the genome during the organism's creation, as well as its initial position, the position of the closest enemy, initial energy level, and numbers that determine in which direction the creature will tend to move. At the end of a life cycle, organisms leave offspring, 0 or from 2 to 4. Mutations also play an important role in population development, we set a certain probability of genome mutation. Thus it adds more opportunities for survival and genome becomes more diverse. 
## How to run the project
можна було б додати короткий модуль типу driver.py де можна вбивати кількість ходів і т.д. і який би чисто генерував мапу для користувача
## Visualisation
![simulation](https://user-images.githubusercontent.com/91615687/171931412-8779f812-15e6-4d3d-9aee-9244c06210b7.gif)
## Results and conclusions
*you can find out more details on code and simulation logic on Wiki pages
