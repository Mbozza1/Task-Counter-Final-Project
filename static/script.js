// Add this function to show the success message
document.addEventListener('DOMContentLoaded', function () {

function showSuccessMessage(tasksLeft) {
  const successMessage = document.getElementById('success-message');
  successMessage.textContent = `Congratulations on finishing a task! You now only have ${tasksLeft} tasks left.`;
  console.log(successMessage)
  successMessage.style.display = 'block';
  successMessage.style.backgroundColor = 'green';
  successMessage.style.color = 'white';
  successMessage.style.padding = '1rem';
  successMessage.style.borderRadius = '4px';
  successMessage.style.marginBottom = '1rem';

  setTimeout(() => {
    successMessage.style.display = 'none';
  }, 3000);
}


document.querySelectorAll('.complete-task').forEach((link, index) => {
  link.addEventListener('click', async (event) => {
    event.preventDefault();
    const taskId = link.getAttribute('data-task-id');
    const taskElement = document.getElementById(`task-${taskId}`);
    
    const tasksLeft = document.querySelectorAll('li').length - 1;
    console.log(taskElement)
    // Removing the task element from the DOM
    showSuccessMessage(tasksLeft);

    // Updating the critter and remove the task
    document.getElementById('critter').textContent = '😃';
    setTimeout(() => {
      document.getElementById('critter').textContent = '🐶';
    }, 3000);


    taskElement.remove();
    // Send a request to the complete_task URL
    const response = await fetch(link.href, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ task_id: taskId })
    });
    



    // Handle errors
    if (!response.ok) {
      console.error(`Error completing task: ${response.statusText}`);
    }
  });
});

});