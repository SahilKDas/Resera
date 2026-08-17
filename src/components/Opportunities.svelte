<script>
  import { onMount } from 'svelte';
  import { apiConfigured, opportunityApi } from '../lib/api.js';

  export let user = null;
  export let onRequestAuth = () => {};

  let opportunities = [];
  let loading = apiConfigured;
  let loadError = '';
  let formOpen = false;
  let submitting = false;
  let success = '';
  let formError = '';
  let form = {
    title: '', organization: '', summary: '', field: 'natural-sciences', location: '',
    remote: false, eligibility: '', deadline: '', source_url: ''
  };

  async function load() {
    if (!apiConfigured) return;
    try {
      opportunities = (await opportunityApi.list()).opportunities;
    } catch (error) {
      loadError = error.message;
    } finally {
      loading = false;
    }
  }

  async function submit() {
    submitting = true;
    formError = '';
    success = '';
    try {
      await opportunityApi.submit(form);
      success = 'Submitted. A Resera moderator will review it before it appears publicly.';
      form = { title: '', organization: '', summary: '', field: 'natural-sciences', location: '', remote: false, eligibility: '', deadline: '', source_url: '' };
      formOpen = false;
    } catch (error) {
      formError = error.message;
    } finally {
      submitting = false;
    }
  }

  onMount(load);
</script>

<section class="opportunities" id="opportunities">
  <div class="opportunities-heading reveal">
    <div class="section-label"><span>03</span> Opportunities</div>
    <h2>Find work worth<br /><em>showing up for.</em></h2>
    <p>Member-submitted research openings, reviewed by Resera moderators before they reach the collective.</p>
    {#if user}
      <button class="button opportunity-action" type="button" on:click={() => formOpen = !formOpen}>{formOpen ? 'Close form' : 'Submit an opportunity'} <span>→</span></button>
    {:else}
      <button class="button opportunity-action" type="button" on:click={onRequestAuth}>Sign in to submit <span>→</span></button>
    {/if}
  </div>

  <div class="opportunity-feed reveal">
    {#if formOpen && user}
      <form class="opportunity-form" on:submit|preventDefault={submit}>
        <div class="form-grid">
          <label>Title<input bind:value={form.title} required maxlength="180" /></label>
          <label>Organization<input bind:value={form.organization} required maxlength="180" /></label>
          <label>Field<select bind:value={form.field}><option value="natural-sciences">Natural sciences</option><option value="technology">Technology</option><option value="humanities">Humanities</option><option value="social-impact">Social impact</option><option value="other">Other</option></select></label>
          <label>Location<input bind:value={form.location} maxlength="180" placeholder="City, country" /></label>
          <label class="full">Summary<textarea bind:value={form.summary} required rows="4"></textarea></label>
          <label>Deadline<input bind:value={form.deadline} type="date" /></label>
          <label>Source URL<input bind:value={form.source_url} type="url" required placeholder="https://" /></label>
          <label class="full">Eligibility<textarea bind:value={form.eligibility} rows="2"></textarea></label>
          <label class="check full"><input bind:checked={form.remote} type="checkbox" /> Remote opportunity</label>
        </div>
        {#if formError}<p class="form-error" role="alert">{formError}</p>{/if}
        <button class="button button-light" type="submit" disabled={submitting}>{submitting ? 'Submitting…' : 'Send for review'} <span>→</span></button>
      </form>
    {/if}

    {#if success}<p class="opportunity-notice success" role="status">{success}</p>{/if}
    {#if loading}
      <p class="opportunity-notice">Looking for approved opportunities…</p>
    {:else if loadError}
      <p class="opportunity-notice">The opportunity service is temporarily unavailable.</p>
    {:else if opportunities.length}
      {#each opportunities as item}
        <article class="opportunity-card">
          <div><span>{item.field_label}</span>{#if item.deadline}<span>Closes {item.deadline}</span>{/if}</div>
          <h3>{item.title}</h3>
          <p class="opportunity-org">{item.organization}{item.location ? ` · ${item.location}` : ''}{item.remote ? ' · Remote' : ''}</p>
          <p>{item.summary}</p>
          <a href={item.source_url} target="_blank" rel="noreferrer">View source <span>↗</span></a>
        </article>
      {/each}
    {:else}
      <div class="opportunity-empty">
        <span>Feed opening soon</span>
        <h3>No approved listings yet.</h3>
        <p>{apiConfigured ? 'Be the first member to submit a research opportunity for review.' : 'The moderated opportunity board will appear when the Resera account service is connected.'}</p>
      </div>
    {/if}
  </div>
</section>
