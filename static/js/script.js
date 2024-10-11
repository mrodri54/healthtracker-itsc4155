document.addEventListener('DOMContentLoaded', function() {

    // Calorie Tracking
    document.getElementById('add-calorie-btn').addEventListener('click', function() {
        const calorieInput = document.getElementById('calorie-input').value;
        if (calorieInput) {
            const listItem = document.createElement('li');
            listItem.textContent = `${calorieInput} kcal`;
            document.getElementById('calorie-list').appendChild(listItem);
            document.getElementById('calorie-input').value = ''; // Clear input
        } else {
            alert('Please enter calorie value!');
        }
    });

    // Sleep Tracking
    document.getElementById('add-sleep-btn').addEventListener('click', function() {
        const sleepInput = document.getElementById('sleep-input').value;
        if (sleepInput) {
            const listItem = document.createElement('li');
            listItem.textContent = `${sleepInput} hours of sleep`;
            document.getElementById('sleep-list').appendChild(listItem);
            document.getElementById('sleep-input').value = ''; // Clear input
        } else {
            alert('Please enter sleep duration!');
        }
    });

    // Habit Tracking
    document.getElementById('add-habit-btn').addEventListener('click', function() {
        const habitInput = document.getElementById('habit-input').value;
        if (habitInput.trim()) {
            const listItem = document.createElement('li');
            listItem.textContent = habitInput;
            document.getElementById('habit-list').appendChild(listItem);
            document.getElementById('habit-input').value = ''; // Clear input
        } else {
            alert('Please enter a habit!');
        }
    });

    // Fitness Tracking
    document.getElementById('add-workout-btn').addEventListener('click', function() {
        const workoutType = document.getElementById('workout-type').value;
        const workoutDuration = document.getElementById('workout-duration').value;
        if (workoutType && workoutDuration) {
            const listItem = document.createElement('li');
            listItem.textContent = `${workoutType} - ${workoutDuration} minutes`;
            document.getElementById('workout-list').appendChild(listItem);
            document.getElementById('workout-type').value = '';
            document.getElementById('workout-duration').value = '';
        } else {
            alert('Please enter workout type and duration!');
        }
    });

    // Water Intake Tracking
    document.getElementById('add-water-btn').addEventListener('click', function() {
        const waterInput = document.getElementById('water-amount').value;
        if (waterInput) {
            const totalWater = document.getElementById('total-water');
            totalWater.textContent = parseFloat(totalWater.textContent) + parseFloat(waterInput);
            document.getElementById('water-amount').value = ''; // Clear input
        } else {
            alert('Please enter water intake value!');
        }
    });

    // Sleep Tracking (Total)
    document.getElementById('add-sleep-btn').addEventListener('click', function() {
        const sleepInput = document.getElementById('sleep-hours').value;
        if (sleepInput) {
            const totalSleep = document.getElementById('total-sleep');
            totalSleep.textContent = parseFloat(totalSleep.textContent) + parseFloat(sleepInput);
            document.getElementById('sleep-hours').value = ''; // Clear input
        } else {
            alert('Please enter sleep hours!');
        }
    });

    // Fitness Tracking: Add workout and calculate calories burned
    document.getElementById('add-workout-btn').addEventListener('click', function() {
        const workoutType = document.getElementById('workout-type').value;
        const workoutDuration = document.getElementById('workout-duration').value;

        if (workoutType && workoutDuration) {
            const workoutElement = document.querySelector(`#workout-type option[value="${workoutType}"]`);
            const caloriesPerMinute = workoutElement.dataset.calories;
            const caloriesBurned = caloriesPerMinute * workoutDuration;

            // Update total calories burned
            const totalCaloriesElement = document.getElementById('total-calories-burned');
            totalCaloriesElement.textContent = parseFloat(totalCaloriesElement.textContent) + parseFloat(caloriesBurned);

            // Add workout to the log
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = `${workoutType} - ${workoutDuration} minutes (${caloriesBurned} kcal burned)`;
            document.getElementById('workout-log').appendChild(listItem);

            // Clear input fields
            document.getElementById('workout-duration').value = '';
        } else {
            alert('Please enter workout type and duration!');
        }
    });

    // Nutrition Tracking: Add food and calculate calories
    document.getElementById('add-food-btn').addEventListener('click', function() {
        const foodType = document.getElementById('food-type').value;
        const foodQuantity = document.getElementById('food-quantity').value;

        if (foodType && foodQuantity) {
            const foodElement = document.querySelector(`#food-type option[value="${foodType}"]`);
            const caloriesPerUnit = foodElement.dataset.calories;
            const caloriesConsumed = caloriesPerUnit * foodQuantity;

            // Update total calories consumed
            const totalCaloriesElement = document.getElementById('total-calories-consumed');
            totalCaloriesElement.textContent = parseFloat(totalCaloriesElement.textContent) + parseFloat(caloriesConsumed);

            // Add food to the log
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = `${foodType} - ${foodQuantity} (${caloriesConsumed} kcal)`;
            document.getElementById('food-log').appendChild(listItem);

            // Clear input fields
            document.getElementById('food-quantity').value = '';
        } else {
            alert('Please enter food type and quantity!');
        }
    });

});
