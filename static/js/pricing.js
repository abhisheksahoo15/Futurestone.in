document.addEventListener("DOMContentLoaded", function () {
    const togglePlan = document.getElementById("togglePlan");
    const monthlyPrices = document.querySelectorAll(".price.monthly");
    const yearlyPrices = document.querySelectorAll(".price.yearly");
    const userRange = document.getElementById("userRange");
    const costDisplay = document.getElementById("cost");
  
    togglePlan.addEventListener("change", function () {
      monthlyPrices.forEach(p => p.style.display = togglePlan.checked ? "none" : "block");
      yearlyPrices.forEach(p => p.style.display = togglePlan.checked ? "block" : "none");
    });
  
    userRange.addEventListener("input", function () {
      const cost = togglePlan.checked ? userRange.value * 15 : userRange.value * 19;
      costDisplay.textContent = `$${cost}`;
    });
  });
  