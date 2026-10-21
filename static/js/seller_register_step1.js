
document.addEventListener('DOMContentLoaded', () => {


  const photoInput = document.getElementById('profile_photo');
  const avatarPreviewBox = document.getElementById('avatarPreviewBox');

  if (photoInput && avatarPreviewBox) {
    photoInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        if (!file.type.startsWith('image/')) {
          alert('Please select a valid image file (JPG, PNG, WEBP).');
          photoInput.value = '';
          return;
        }
        const reader = new FileReader();
        reader.onload = (evt) => {
          avatarPreviewBox.innerHTML = `<img src="${evt.target.result}" alt="Profile Preview">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  const mobileInput = document.getElementById('mobile');
  const mobileOtpBtn = document.getElementById('mobileOtpBtn');
  const mobileOtpGroup = document.getElementById('mobileOtpGroup');
  const mobileOtpInput = document.getElementById('mobile_otp_input');
  const mobileStatusBadge = document.getElementById('mobileStatusBadge');
  const mobileVerifiedHidden = document.getElementById('mobile_verified');

  let simulatedMobileOtp = '';
  let mobileTimer = null;

  if (mobileVerifiedHidden && mobileVerifiedHidden.value === 'true') {
    if (mobileStatusBadge) mobileStatusBadge.style.display = 'inline-flex';
    if (mobileOtpGroup) mobileOtpGroup.classList.add('show');
    if (mobileOtpBtn) {
      mobileOtpBtn.textContent = 'Verified ✓';
      mobileOtpBtn.disabled = true;
    }
  }

  if (mobileInput) {
    mobileInput.addEventListener('input', () => {
      if (mobileVerifiedHidden && mobileVerifiedHidden.value === 'true') {
        mobileVerifiedHidden.value = 'false';
        if (mobileStatusBadge) mobileStatusBadge.style.display = 'none';
        if (mobileOtpBtn) {
          mobileOtpBtn.textContent = 'OTP';
          mobileOtpBtn.disabled = false;
        }
        if (mobileOtpInput) {
          mobileOtpInput.style.borderColor = '';
          mobileOtpInput.value = '';
        }
        simulatedMobileOtp = '';
      }
    });
  }

  if (mobileOtpBtn) {
    mobileOtpBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const num = mobileInput ? mobileInput.value.trim() : '';

      if (!num || num.length < 10) {
        alert('Please enter a valid 10-digit Mobile Number before requesting OTP.');
        if (mobileInput) mobileInput.focus();
        return;
      }

      simulatedMobileOtp = Math.floor(100000 + Math.random() * 900000).toString();
      alert(`[THEIR NIBS OTP SERVICE]\nYour verification OTP for Mobile Number ${num} is: ${simulatedMobileOtp}`);

      if (mobileOtpGroup) {
        mobileOtpGroup.classList.add('show');
      }
      if (mobileOtpInput) {
        mobileOtpInput.value = '';
        mobileOtpInput.placeholder = 'Enter 6-digit OTP';
        mobileOtpInput.focus();
      }

      let secondsLeft = 30;
      mobileOtpBtn.disabled = true;
      clearInterval(mobileTimer);
      mobileTimer = setInterval(() => {
        secondsLeft--;
        if (secondsLeft <= 0) {
          clearInterval(mobileTimer);
          mobileOtpBtn.disabled = false;
          mobileOtpBtn.textContent = 'Resend OTP';
        } else {
          mobileOtpBtn.textContent = `Resend in ${secondsLeft}s`;
        }
      }, 1000);
    });
  }

  if (mobileOtpInput) {
    mobileOtpInput.addEventListener('input', () => {
      const val = mobileOtpInput.value.trim();
      if (val === simulatedMobileOtp && val !== '') {
        if (mobileStatusBadge) mobileStatusBadge.style.display = 'inline-flex';
        if (mobileVerifiedHidden) mobileVerifiedHidden.value = 'true';
        mobileOtpInput.style.borderColor = 'var(--color-success-green)';
        if (mobileOtpBtn) {
          mobileOtpBtn.textContent = 'Verified ✓';
          mobileOtpBtn.disabled = true;
        }
        clearInterval(mobileTimer);
      }
    });
  }

  const emailInput = document.getElementById('email');
  const emailOtpBtn = document.getElementById('emailOtpBtn');
  const emailOtpGroup = document.getElementById('emailOtpGroup');
  const emailOtpInput = document.getElementById('email_otp_input');
  const emailStatusBadge = document.getElementById('emailStatusBadge');
  const emailVerifiedHidden = document.getElementById('email_verified');

  let simulatedEmailOtp = '';
  let emailTimer = null;

  if (emailVerifiedHidden && emailVerifiedHidden.value === 'true') {
    if (emailStatusBadge) emailStatusBadge.style.display = 'inline-flex';
    if (emailOtpGroup) emailOtpGroup.classList.add('show');
    if (emailOtpBtn) {
      emailOtpBtn.textContent = 'Verified ✓';
      emailOtpBtn.disabled = true;
    }
  }

  if (emailInput) {
    emailInput.addEventListener('input', () => {
      if (emailVerifiedHidden && emailVerifiedHidden.value === 'true') {
        emailVerifiedHidden.value = 'false';
        if (emailStatusBadge) emailStatusBadge.style.display = 'none';
        if (emailOtpBtn) {
          emailOtpBtn.textContent = 'OTP';
          emailOtpBtn.disabled = false;
        }
        if (emailOtpInput) {
          emailOtpInput.style.borderColor = '';
          emailOtpInput.value = '';
        }
        simulatedEmailOtp = '';
      }
    });
  }

  if (emailOtpBtn) {
    emailOtpBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const mail = emailInput ? emailInput.value.trim() : '';

      if (!mail || !mail.includes('@')) {
        alert('Please enter a valid Email Address before requesting OTP.');
        if (emailInput) emailInput.focus();
        return;
      }

      simulatedEmailOtp = Math.floor(100000 + Math.random() * 900000).toString();
      alert(`[THEIR NIBS OTP SERVICE]\nYour verification OTP for Email Address ${mail} is: ${simulatedEmailOtp}`);

      if (emailOtpGroup) {
        emailOtpGroup.classList.add('show');
      }
      if (emailOtpInput) {
        emailOtpInput.value = '';
        emailOtpInput.placeholder = 'Enter 6-digit OTP';
        emailOtpInput.focus();
      }

      let secondsLeft = 30;
      emailOtpBtn.disabled = true;
      clearInterval(emailTimer);
      emailTimer = setInterval(() => {
        secondsLeft--;
        if (secondsLeft <= 0) {
          clearInterval(emailTimer);
          emailOtpBtn.disabled = false;
          emailOtpBtn.textContent = 'Resend OTP';
        } else {
          emailOtpBtn.textContent = `Resend in ${secondsLeft}s`;
        }
      }, 1000);
    });
  }

  if (emailOtpInput) {
    emailOtpInput.addEventListener('input', () => {
      const val = emailOtpInput.value.trim();
      if (val === simulatedEmailOtp && val !== '') {
        if (emailStatusBadge) emailStatusBadge.style.display = 'inline-flex';
        if (emailVerifiedHidden) emailVerifiedHidden.value = 'true';
        emailOtpInput.style.borderColor = 'var(--color-success-green)';
        if (emailOtpBtn) {
          emailOtpBtn.textContent = 'Verified ✓';
          emailOtpBtn.disabled = true;
        }
        clearInterval(emailTimer);
      }
    });
  }

  
  const idTypeSelect = document.getElementById('id_type');
  const idNumberInput = document.getElementById('id_number');

  const idPlaceholders = {
    'Aadhaar': 'Enter 12-digit Aadhaar Number (e.g. 9876 5432 1098)',
    'PAN': 'Enter 10-character PAN (e.g. ABCDE1234F)',
    'Passport': 'Enter Passport Number (e.g. Z1234567)',
    'Driving Licence': 'Enter Driving Licence Number (e.g. DL-1420110012345)',
    'Voter ID': 'Enter Voter ID Number (EPIC)'
  };

  if (idTypeSelect && idNumberInput) {
    idTypeSelect.addEventListener('change', () => {
      const selected = idTypeSelect.value;
      idNumberInput.placeholder = idPlaceholders[selected] || 'Enter selected ID Number';
    });
  }

  
  const roleRadios = document.querySelectorAll('input[name="applicant_role"]');
  const authLetterBox = document.getElementById('authorizationLetterBox');
  const authLetterInput = document.getElementById('authorization_letter');

  function checkRoleConditional() {
    let selectedValue = '';
    roleRadios.forEach(radio => {
      if (radio.checked) selectedValue = radio.value;
    });

    if (selectedValue === 'Authorized Representative') {
      authLetterBox.classList.add('show');
      authLetterInput.setAttribute('required', 'required');
    } else {
      authLetterBox.classList.remove('show');
      authLetterInput.removeAttribute('required');
    }
  }

  roleRadios.forEach(radio => {
    radio.addEventListener('change', checkRoleConditional);
  });
 
  checkRoleConditional();

  
  const documentUploadInputs = document.querySelectorAll('input[type="file"]:not(#profile_photo)');
  documentUploadInputs.forEach(fileInput => {
    fileInput.addEventListener('change', () => {
      const infoEl = fileInput.parentElement.querySelector('.file-preview-info');
      if (infoEl && fileInput.files.length > 0) {
        infoEl.textContent = `Attached File: ${fileInput.files[0].name}`;
      }
    });
  });

  
  const sameAsPresentCheckbox = document.getElementById('same_as_present');
  const presentAddress = document.getElementById('present_address');
  const presentState = document.getElementById('present_state');
  const presentDistrict = document.getElementById('present_district');
  const presentPincode = document.getElementById('present_pincode');

  const permanentAddress = document.getElementById('permanent_address');
  const permanentState = document.getElementById('permanent_state');
  const permanentDistrict = document.getElementById('permanent_district');
  const permanentPincode = document.getElementById('permanent_pincode');

  function syncPresentToPermanent() {
    if (!sameAsPresentCheckbox || !sameAsPresentCheckbox.checked) return;

    if (presentAddress && permanentAddress) permanentAddress.value = presentAddress.value;
    if (presentState && permanentState) permanentState.value = presentState.value;
    if (presentDistrict && permanentDistrict) permanentDistrict.value = presentDistrict.value;
    if (presentPincode && permanentPincode) permanentPincode.value = presentPincode.value;
  }

  function setPermanentReadOnlyState(isReadOnly) {
    const permElements = [permanentAddress, permanentState, permanentDistrict, permanentPincode];
    permElements.forEach(el => {
      if (!el) return;
      if (isReadOnly) {
        el.setAttribute('readonly', 'readonly');
        if (el.tagName === 'SELECT') {
          el.style.pointerEvents = 'none';
          el.style.backgroundColor = '#f1f5f9';
        } else {
          el.style.backgroundColor = '#f1f5f9';
        }
      } else {
        el.removeAttribute('readonly');
        if (el.tagName === 'SELECT') {
          el.style.pointerEvents = 'auto';
          el.style.backgroundColor = '#ffffff';
        } else {
          el.style.backgroundColor = '#ffffff';
        }
      }
    });
  }

  if (sameAsPresentCheckbox) {
    sameAsPresentCheckbox.addEventListener('change', () => {
      if (sameAsPresentCheckbox.checked) {
        syncPresentToPermanent();
        setPermanentReadOnlyState(true);
      } else {
        setPermanentReadOnlyState(false);
      }
    });

    [presentAddress, presentState, presentDistrict, presentPincode].forEach(el => {
      if (!el) return;
      ['input', 'change'].forEach(evtType => {
        el.addEventListener(evtType, () => {
          if (sameAsPresentCheckbox.checked) {
            syncPresentToPermanent();
          }
        });
      });
    });
  }


  const pwdInput = document.getElementById('password');
  const confirmPwdInput = document.getElementById('confirm_password');
  const pwdErrBox = document.getElementById('passwordMatchError');
  const step1Form = document.querySelector('form.form-card');

  function validatePasswordMatch() {
    if (!pwdInput || !confirmPwdInput) return true;
    const pwd = pwdInput.value;
    const confirmPwd = confirmPwdInput.value;

    if (confirmPwd.length > 0 && pwd !== confirmPwd) {
      if (pwdErrBox) pwdErrBox.style.display = 'block';
      confirmPwdInput.style.borderColor = '#dc2626';
      return false;
    } else {
      if (pwdErrBox) pwdErrBox.style.display = 'none';
      if (confirmPwd.length > 0 && pwd === confirmPwd) {
        confirmPwdInput.style.borderColor = 'var(--color-success-green)';
      } else {
        confirmPwdInput.style.borderColor = 'var(--color-border)';
      }
      return true;
    }
  }

  if (pwdInput && confirmPwdInput) {
    pwdInput.addEventListener('input', validatePasswordMatch);
    confirmPwdInput.addEventListener('input', validatePasswordMatch);
  }

  if (step1Form) {
    step1Form.addEventListener('submit', (e) => {
      if (!validatePasswordMatch()) {
        e.preventDefault();
        alert('Passwords do not match. Please ensure both Password and Confirm Password fields are identical.');
        confirmPwdInput.focus();
        return false;
      }
    });
  }

});


function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const eyeOpenSVG = `<svg class="eye-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
  const eyeOffSVG = `<svg class="eye-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;

  if (input.type === 'password') {
    input.type = 'text';
    btn.innerHTML = eyeOffSVG;
    btn.setAttribute('aria-label', 'Hide Password');
  } else {
    input.type = 'password';
    btn.innerHTML = eyeOpenSVG;
    btn.setAttribute('aria-label', 'Show Password');
  }
}

