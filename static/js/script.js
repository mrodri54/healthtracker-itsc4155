document.addEventListener('DOMContentLoaded', function() {
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (localStorage.getItem('theme') === 'dark') {
        enableDarkMode();
    }
    darkModeToggle.addEventListener('click', toggleDarkMode);

    function enableDarkMode() {
        document.body.classList.add('dark-mode');
        darkModeToggle.textContent = 'Light Mode';
        document.querySelectorAll('.nav-item').forEach(item => item.classList.add('dark-mode'));
    }

    function disableDarkMode() {
        document.body.classList.remove('dark-mode');
        darkModeToggle.textContent = 'Dark Mode';
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('dark-mode'));
    }

    function toggleDarkMode() {
        if (document.body.classList.contains('dark-mode')) {
            disableDarkMode();
            localStorage.setItem('theme', 'light');
        } else {
            enableDarkMode();
            localStorage.setItem('theme', 'dark');
        }
    }

    // Calorie Tracker
    const calorieInput = document.getElementById('calorie-input');
    document.getElementById('add-calorie-btn')?.addEventListener('click', function() {
        if (calorieInput && calorieInput.value) {
            addToLog('calorie-list', `${calorieInput.value} kcal`);
            calorieInput.value = ''; // Clear input
        } else {
            alert('Please enter a calorie value!');
        }
    });

    // Food Intake Tracker with Nutritional Breakdown
    let totalCalories = 0, totalProtein = 0, totalCarbs = 0, totalFat = 0;
    document.getElementById('add-food-btn')?.addEventListener('click', function() {
        const foodSelect = document.getElementById('food-type');
        const foodQuantity = parseFloat(document.getElementById('food-quantity')?.value || 0);

        if (foodSelect && foodQuantity) {
            const foodData = foodSelect.selectedOptions[0].dataset;
            const calories = foodData.calories * foodQuantity;
            const protein = foodData.protein * foodQuantity;
            const carbs = foodData.carbs * foodQuantity;
            const fat = foodData.fat * foodQuantity;

            totalCalories += calories;
            totalProtein += protein;
            totalCarbs += carbs;
            totalFat += fat;

            document.getElementById('total-food-calories').textContent = totalCalories.toFixed(2);
            addToLog('food-log', `${foodSelect.value} - ${foodQuantity} servings (${calories.toFixed(2)} kcal, ${protein.toFixed(2)}g protein, ${carbs.toFixed(2)}g carbs, ${fat.toFixed(2)}g fat)`);

            document.getElementById('food-quantity').value = '';
        } else {
            alert('Please select a food type and enter a quantity!');
        }
    });

    // Workout Tracker with Calories Burned Calculation
    let totalWorkoutCalories = 0;
    document.getElementById('add-workout-btn')?.addEventListener('click', function() {
        const workoutTypeSelect = document.getElementById('workout-type');
        const workoutDuration = parseInt(document.getElementById('workout-duration')?.value || 0, 10);

        if (workoutTypeSelect && workoutDuration) {
            const caloriesPerMinute = parseInt(workoutTypeSelect.selectedOptions[0].dataset.calories, 10);
            const caloriesBurned = caloriesPerMinute * workoutDuration;
            totalWorkoutCalories += caloriesBurned;

            document.getElementById('total-calories-burned').textContent = totalWorkoutCalories.toFixed(2);
            addToLog('workout-log', `${workoutTypeSelect.value} - ${workoutDuration} minutes (${caloriesBurned} kcal burned)`);

            document.getElementById('workout-duration').value = '';
        } else {
            alert('Please select a workout type and enter a duration!');
        }
    });

    // Water Intake Tracker
    let totalWaterIntake = 0;
    document.getElementById('add-water-btn')?.addEventListener('click', function() {
        const waterAmount = parseFloat(document.getElementById('water-amount')?.value || 0);
        const waterUnit = document.getElementById('water-unit')?.value || 'liters';
        if (waterAmount) {
            totalWaterIntake += waterAmount;
            document.getElementById('total-water').textContent = `${totalWaterIntake.toFixed(2)} ${waterUnit}`;
            document.getElementById('water-amount').value = '';
        } else {
            alert('Please enter a water intake amount!');
        }
    });

    // Sleep Tracker
    let totalSleepHours = 0;
    document.getElementById('add-sleep-btn')?.addEventListener('click', function() {
        const sleepHours = parseFloat(document.getElementById('sleep-hours')?.value || 0);
        if (sleepHours) {
            totalSleepHours += sleepHours;
            document.getElementById('total-sleep').textContent = `${totalSleepHours.toFixed(2)} hours`;
            document.getElementById('sleep-hours').value = '';
        } else {
            alert('Please enter sleep hours!');
        }
    });

    // Helper function to add items to logs
    function addToLog(logId, text) {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item');
        listItem.textContent = text;
        document.getElementById(logId).appendChild(listItem);
    }
});
