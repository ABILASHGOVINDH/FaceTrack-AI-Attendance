document.getElementById('attendanceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally
    const name = document.getElementById('name').value;
    const date = document.getElementById('date').value;

    if (!name || !date) {
        alert('Please fill the details');
    } else {
        // Proceed with form submission or other logic here
        alert('Details submitted successfully!');
    }
});


function validateLoginForm() {
            var id = document.getElementById("enter_your_id").value;
            var name = document.getElementById("name").value;
            var password = document.getElementById("password").value;

            if (id.trim() === "") {
                alert("Please fill the 'Enter Your Id' field.");
                return false;
            }
            if (name.trim() === "") {
                alert("Please fill the 'Name' field.");
                return false;
            }
            if (password.trim() === "") {
                alert("Please fill the 'Password' field.");
                return false;
            }
            return true;
        }