
document.addEventListener('DOMContentLoaded', () => {

  
  const differentPickupRadios = document.querySelectorAll('input[name="different_pickup"]');
  const pickupAddressBox = document.getElementById('pickupAddressBox');
  const pickupAddressInput = document.getElementById('pickup_address');
  const pickupCityInput = document.getElementById('pickup_city');
  const pickupStateSelect = document.getElementById('pickup_state');
  const pickupPincodeInput = document.getElementById('pickup_pincode');

  function checkPickupConditional() {
    let isDifferent = false;
    differentPickupRadios.forEach(radio => {
      if (radio.checked && radio.value === 'Yes') isDifferent = true;
    });

    if (isDifferent) {
      pickupAddressBox.classList.add('show');
      if (pickupAddressInput) pickupAddressInput.setAttribute('required', 'required');
      if (pickupCityInput) pickupCityInput.setAttribute('required', 'required');
      if (pickupStateSelect) pickupStateSelect.setAttribute('required', 'required');
      if (pickupPincodeInput) pickupPincodeInput.setAttribute('required', 'required');
    } else {
      pickupAddressBox.classList.remove('show');
      if (pickupAddressInput) pickupAddressInput.removeAttribute('required');
      if (pickupCityInput) pickupCityInput.removeAttribute('required');
      if (pickupStateSelect) pickupStateSelect.removeAttribute('required');
      if (pickupPincodeInput) pickupPincodeInput.removeAttribute('required');
    }
  }

  differentPickupRadios.forEach(radio => {
    radio.addEventListener('change', checkPickupConditional);
  });
 
  checkPickupConditional();

  
  const gstRadios = document.querySelectorAll('input[name="gst_registered"]');
  const gstinBox = document.getElementById('gstinBox');
  const gstinInput = document.getElementById('gstin');

  function checkGstConditional() {
    let isGstYes = false;
    gstRadios.forEach(radio => {
      if (radio.checked && radio.value === 'Yes') isGstYes = true;
    });

    if (isGstYes) {
      gstinBox.classList.add('show');
      if (gstinInput) gstinInput.setAttribute('required', 'required');
    } else {
      gstinBox.classList.remove('show');
      if (gstinInput) gstinInput.removeAttribute('required');
    }
  }

  gstRadios.forEach(radio => {
    radio.addEventListener('change', checkGstConditional);
  });
  
  checkGstConditional();

});
