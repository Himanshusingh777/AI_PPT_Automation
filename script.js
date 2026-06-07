let form = document.getElementById("form")

form.addEventListener(
    "submit",

    async(e) => {

        e.preventDefault()

        let fd = new FormData(form)

        document.getElementById(
                "output"
            ).innerHTML =
            `
<h2>Processing...</h2>
`

        let response =

            await fetch(
                "/generate", {
                    method: "POST",
                    body: fd
                }
            )

        let data =
            await response.json()

        document.getElementById(
            "output"
        ).innerHTML = `

<div class="card">

<h2>
Step1 Research
</h2>

<button onclick="copyText('r')">
Copy
</button>

<pre id="r">
${data.step1}
</pre>

</div>



<div class="card">

<h2>
Step2 Slides
</h2>

<button onclick="copyText('s')">
Copy
</button>

<pre id="s">
${data.step2}
</pre>

</div>



<div class="card">

<h2>
Step3 Detailed
</h2>

<button onclick="copyText('d')">
Copy
</button>

<pre id="d">
${data.step3}
</pre>

</div>



<div class="card">

<h2>
Step4 Human Mail
</h2>

<button onclick="copyText('e')">
Copy
</button>

<pre id="e">
${data.step4}
</pre>

</div>

`

    }

)


function copyText(id) {

    let txt =
        document.getElementById(
            id
        ).innerText

    navigator.clipboard.writeText(
        txt
    )

    alert(
        "Copied"
    )

}