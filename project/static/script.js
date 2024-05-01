const formOpenBtn = document.querySelector("#form-open"),
  home = document.querySelector(".home"),
  formContainer = document.querySelector(".form_container"),
  formCloseBtn = document.querySelector(".form_close"),
  signupBtn = document.querySelector("#signup"),
  loginBtn = document.querySelector("#login"),
  pwShowHide = document.querySelectorAll(".pw_hide");

formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));

pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});

signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
});
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
});

const humans_parent = document.getElementById("humans");
const BLOOD_TYPES = {
  "O−": ["O−", "O+", "A−", "A+", "B−", "B+", "AB−", "AB+"],
  "O+": ["O+", "A+", "B+", "AB+"],
  "A−": ["A−", "A+", "AB−", "AB+"],
  "A+": ["A+", "AB+"],
  "B−": ["B−", "B+", "AB−", "AB+"],
  "B+": ["B+", "AB+"],
  "AB−": ["AB−", "AB+"],
  "AB+": ["AB+"]
};
const reset_button = document.getElementById("reset");
const selector = document.getElementById("blood_selector");
const blood_vias = document.querySelectorAll("#humans .human .blood_via");
const blood_bag = document.querySelector("#blood_content > div.main_bag > div");
const center_via = document.querySelector(".center_via > .blood_via");
const blood_types = document.querySelectorAll(".blood_type");
let lastCalled;
addListeners();

function callIfChildren(e) {
  if (lastCalled) change();
  if (e.target !== this) setRecipents(e);
}

function addListeners() {
  selector.addEventListener("click", callIfChildren);
  reset.addEventListener("click", reset);
}

function reset() {
  change();
  blood_bag.style.height = "100px";
  center_via.style.height = "0px";
}

function change() {
  lastCalled.target.classList.remove("highlight");

  for (let i = 0; i < blood_vias.length; i++) {
    blood_vias[i].style.width = "0px";
    blood_types[i].classList.remove("highlightText");
  }
}

function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function setRecipents(e) {
  e.target.classList.add("highlight");
  lastCalled = e;

  const donor = e.target.innerText;
  for (let item of BLOOD_TYPES[donor]) {
    const recipent_index = Object.keys(BLOOD_TYPES).indexOf(item);
    const height = 50 + 50 * Math.floor(recipent_index / 2);
    const blood_height = 125 - 25 * Math.floor(recipent_index / 2);
    blood_bag.style.height = `${blood_height}px`;
    center_via.style.height = `${height}px`;

    await timeout(100);
    blood_vias[recipent_index].style.width = "100%";
    blood_types[recipent_index].classList.add("highlightText");
  }
}

feather.replace();
