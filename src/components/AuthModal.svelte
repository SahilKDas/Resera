<script>
  import { authApi, apiConfigured } from '../lib/api.js';
  export let open = false;
  export let user = null;
  export let onClose = () => {};
  export let onAuthenticated = () => {};
  let mode = 'login';
  let username = '';
  let email = '';
  let password = '';
  let passwordConfirm = '';
  let error = '';
  let busy = false;

  async function submit() {
    error = '';
    busy = true;
    try {
      const payload = mode === 'login'
        ? await authApi.login({ username, password })
        : await authApi.register({ username, email, password, password_confirm: passwordConfirm });
      onAuthenticated(payload.user);
      password = '';
      passwordConfirm = '';
      onClose();
    } catch (requestError) {
      error = requestError.message;
    } finally {
      busy = false;
    }
  }

  async function signOut() {
    busy = true;
    error = '';
    try {
      await authApi.logout();
      onAuthenticated(null);
      onClose();
    } catch (requestError) {
      error = requestError.message;
    } finally {
      busy = false;
    }
  }

  function changeMode(nextMode) {
    mode = nextMode;
    error = '';
  }

  function handleKeydown(event) {
    if (open && event.key === 'Escape') onClose();
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div class="modal-backdrop" role="presentation" on:click={(event) => event.currentTarget === event.target && onClose()}>
    <section class="auth-modal" role="dialog" aria-modal="true" aria-labelledby="auth-title">
      <button class="modal-close" type="button" on:click={onClose} aria-label="Close account dialog">×</button>
      <p class="eyebrow"><span></span> Member access</p>
      {#if user}
        <h2 id="auth-title">Welcome back,<br /><em>{user.username}.</em></h2>
        <p class="modal-copy">Your Resera account is active. You can submit research opportunities for moderator review.</p>
        <button class="button button-light" type="button" disabled={busy} on:click={signOut}>Sign out <span>→</span></button>
      {:else if !apiConfigured}
        <h2 id="auth-title">Accounts are<br /><em>coming online.</em></h2>
        <p class="modal-copy">The Django account service is built, but it has not been connected to this public GitHub Pages deployment yet.</p>
        <button class="button button-light" type="button" on:click={onClose}>Got it <span>→</span></button>
      {:else}
        <div class="auth-tabs" aria-label="Account action">
          <button class:active={mode === 'login'} type="button" on:click={() => changeMode('login')}>Sign in</button>
          <button class:active={mode === 'register'} type="button" on:click={() => changeMode('register')}>Create account</button>
        </div>
        <h2 id="auth-title">{mode === 'login' ? 'Dive back in.' : 'Join the collective.'}</h2>
        <form on:submit|preventDefault={submit}>
          <label>Username<input bind:value={username} autocomplete="username" required maxlength="150" /></label>
          {#if mode === 'register'}<label>Email<input bind:value={email} type="email" autocomplete="email" required /></label>{/if}
          <label>Password<input bind:value={password} type="password" autocomplete={mode === 'login' ? 'current-password' : 'new-password'} required /></label>
          {#if mode === 'register'}<label>Confirm password<input bind:value={passwordConfirm} type="password" autocomplete="new-password" required /></label>{/if}
          {#if error}<p class="form-error" role="alert">{error}</p>{/if}
          <button class="button button-light" type="submit" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'} <span>→</span></button>
        </form>
      {/if}
      {#if error && (user || !apiConfigured)}<p class="form-error" role="alert">{error}</p>{/if}
    </section>
  </div>
{/if}
