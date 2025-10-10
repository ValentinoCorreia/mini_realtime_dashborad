/**
 * @type {HTMLInputElement}
 */
const USERNAME_INPUT = document.getElementById("username_input");
/**
 * @type {HTMLInputElement}
 */
const PASSWORD_INPUT = document.getElementById("password_input");

document.getElementById("login_form").addEventListener(
    "submit",
    ev => {
        ev.preventDefault();
        
        const data = {
            username: USERNAME_INPUT.value,
            password: PASSWORD_INPUT.value
        }
        const req_headers = new Headers()
        req_headers.set("Content-Type", "application/json")
        fetch("#",
            {
                method: "POST",
                headers: req_headers,
                body: JSON.stringify(data)
            }
        )
        .then(resp => {
            if (resp.status === 200) {
                resp.json().then(json => {
                    localStorage.setItem("token" ,json.token)
                    location.replace("/dashboard")
                })
            }
            else {
                document.querySelector("p.warn").innerHTML = "Invalid login"
                console.warn("status code request: " + resp.status)
            }
        })
    }
)