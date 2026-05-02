const API_URL = "http://127.0.0.1:8000";

// Load all courses
async function loadCourses() {
    const res = await fetch(`${API_URL}/courses`);
    const data = await res.json();
    displayCourses(data);
}

// Display courses
function displayCourses(courses) {
    const container = document.getElementById("courseList");
    container.innerHTML = "";

    courses.forEach(course => {
        const div = document.createElement("div");
        div.className = "course";

        div.innerHTML = `
            <h3>${course.title}</h3>
            <p>Instructor: ${course.instructor}</p>
            <p>Price: ₹${course.price}</p>
            <p>Category: ${course.category}</p>
            <button onclick="deleteCourse(${course.id})" class="delete-btn">Delete</button>
        `;

        container.appendChild(div);
    });
}

// Add Course
async function addCourse() {
    const course = {
        title: document.getElementById("title").value,
        instructor: document.getElementById("instructor").value,
        category: document.getElementById("category").value,
        price: parseFloat(document.getElementById("price").value),
        duration_hours: parseInt(document.getElementById("duration").value),
        discount_percent: parseFloat(document.getElementById("discount").value),
        is_published: false
    };

    await fetch(`${API_URL}/courses`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(course)
    });

    loadCourses();
}

// Delete Course
async function deleteCourse(id) {
    await fetch(`${API_URL}/courses/${id}`, {
        method: "DELETE"
    });

    loadCourses();
}

// Filter Courses
async function filterCourses() {
    const maxPrice = document.getElementById("maxPrice").value;

    const res = await fetch(`${API_URL}/courses/filter/search?max_price=${maxPrice}`);
    const data = await res.json();

    displayCourses(data.courses);
}

// Initial Load
loadCourses();