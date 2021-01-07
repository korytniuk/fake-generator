function setSelectedManually(element) {
  element.options[element.selectedIndex].setAttribute("selected", "");
}

function toggleRange(element) {
  nodes = element.closest(".form-row").querySelectorAll(".range");
  if ([2, 4].some((x) => x === element.selectedIndex)) {
    nodes.forEach((e) => {
      e.classList.remove("d-none");
    });
  } else {
    nodes.forEach((e) => {
      e.classList.add("d-none");
    });
  }
}

function showRange() {
  const nodes = document.querySelectorAll(".range");
  nodes.forEach((e) => {
    if (e.querySelector("input").value !== "") {
      e.classList.remove("d-none");
    }
  });
}

function handleSchemaForm() {
  showRange();
  const columns = document.querySelectorAll(".column-row");
  const container = document.querySelector("form");
  const addButton = document.querySelector("#add-column");
  const totalForms = document.querySelector("#id_columns-TOTAL_FORMS");

  let formNum = columns.length - 1;

  document.querySelector("body").addEventListener("change", (e) => {
    if (e.target.tagName == "SELECT") {
      toggleRange(e.target);
    }
  });

  //use for cloning
  const templateColumn = columns[columns.length - 1].cloneNode(true);

  addButton.addEventListener("click", addColumn);

  function addColumn(e) {
    e.preventDefault();

    const newForm = templateColumn.cloneNode(true);
    const formRegex = RegExp(`columns-(\\d){1}-`, "g");
    formNum++; //Increment the form number

    newForm.innerHTML = newForm.innerHTML.replace(
      formRegex,
      `columns-${formNum}-`
    );
    container.insertBefore(newForm, addButton);
    totalForms.setAttribute("value", `${formNum + 1}`);
  }
}
