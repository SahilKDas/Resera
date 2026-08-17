<script>
  import { onMount } from 'svelte';
  import AuthModal from './components/AuthModal.svelte';
  import Opportunities from './components/Opportunities.svelte';
  import { apiConfigured, authApi } from './lib/api.js';

  let menuOpen = false;
  let navScrolled = false;
  let authOpen = false;
  let currentUser = null;
  const asset = (file) => `${import.meta.env.BASE_URL}${file}`;

  const fields = [
    { number: '01', title: 'Natural Sciences', text: 'From living systems to the physics shaping our universe.' },
    { number: '02', title: 'Technology', text: 'Building, testing, and questioning the tools defining tomorrow.' },
    { number: '03', title: 'Humanities', text: 'Understanding the stories, systems, and ideas that move people.' },
    { number: '04', title: 'Social Impact', text: 'Research designed to make communities stronger and more just.' }
  ];

  const process = [
    { step: '01', title: 'Bring a question', text: 'Start with the thing you cannot stop wondering about. It does not need to be polished yet.' },
    { step: '02', title: 'Find your people', text: 'Connect with peers and mentors who challenge your assumptions and strengthen your approach.' },
    { step: '03', title: 'Follow the evidence', text: 'Build the habits, methods, and source trail that turn an idea into work you can stand behind.' },
    { step: '04', title: 'Share what you found', text: 'Publish, present, and contribute your perspective to a wider community of young researchers.' }
  ];

  function closeMenu() {
    menuOpen = false;
  }

  function openAccount() {
    closeMenu();
    authOpen = true;
  }

  onMount(() => {
    if (apiConfigured) {
      authApi.me().then((response) => currentUser = response.user).catch(() => currentUser = null);
    }

    const updateNav = () => navScrolled = window.scrollY > 36;
    updateNav();
    window.addEventListener('scroll', updateNav, { passive: true });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('is-visible');
      });
    }, { threshold: 0.16 });
    document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));

    return () => {
      window.removeEventListener('scroll', updateNav);
      observer.disconnect();
    };
  });
</script>

<svelte:head>
  <meta name="color-scheme" content="dark" />
</svelte:head>

<header class:scrolled={navScrolled}>
  <a class="brand" href="#home" aria-label="RESERA home" on:click={closeMenu}>
    <span class="brand-mark" style={`background-image: url('${asset('resera-logo.png')}')`}></span>
    <span>RESERA</span>
  </a>

  <button class="menu-button" class:open={menuOpen} on:click={() => menuOpen = !menuOpen} aria-label="Toggle navigation" aria-expanded={menuOpen}>
    <span></span><span></span>
  </button>

  <nav class:open={menuOpen} aria-label="Main navigation">
    <a href="#about" on:click={closeMenu}>About</a>
    <a href="#explore" on:click={closeMenu}>Explore</a>
    <a href="#opportunities" on:click={closeMenu}>Opportunities</a>
    <a href="#process" on:click={closeMenu}>How it works</a>
    <button class="nav-account-mobile" type="button" on:click={openAccount}>{currentUser ? `@${currentUser.username}` : 'Member sign in'}</button>
  </nav>

  <div class="header-actions">
    <button class="account-button" type="button" on:click={openAccount}>{currentUser ? `@${currentUser.username}` : 'Sign in'}</button>
    <a class="nav-cta" href="https://discord.gg/kJWRfURJY3" target="_blank" rel="noreferrer">Join <span>↗</span></a>
  </div>
</header>

<main>
  <section class="hero" id="home">
    <div class="hero-image" aria-hidden="true"></div>
    <div class="hero-shade" aria-hidden="true"></div>
    <div class="bubbles" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>

    <div class="hero-content">
      <p class="eyebrow hero-eyebrow"><span></span> Student-led research collective</p>
      <h1>Go beyond<br />the <em>surface.</em></h1>
      <p class="hero-copy">For young thinkers ready to ask harder questions, find better evidence, and make discoveries that matter.</p>
      <div class="hero-actions">
        <a class="button button-light" href="#about">Discover RESERA <span>↓</span></a>
        <a class="text-link" href="#opportunities">View opportunities <span>↗</span></a>
      </div>
    </div>

    <div class="member-proof"><strong>1,050+</strong><span>members<br />and growing</span></div>
    <div class="hero-side-label">Curiosity has no depth limit</div>
    <div class="scroll-note"><span>Scroll to descend</span><i></i></div>
  </section>

  <section class="manifesto" id="about">
    <div class="section-label reveal"><span>01</span> About RESERA</div>
    <div class="manifesto-grid">
      <p class="manifesto-kicker reveal">The questions worth asking<br />rarely have easy answers.</p>
      <div class="manifesto-copy reveal">
        <h2>We help students turn<br /><em>curiosity into contribution.</em></h2>
        <p>RESERA is a student-led research collective of more than 1,050 members and growing. We create the space, community, and structure to take an idea seriously—from its first uncertain question to work worth sharing.</p>
        <a class="arrow-link" href="#process">How we work <span>→</span></a>
      </div>
    </div>
    <div class="statement reveal">
      <span>We believe research should feel less like a closed door</span>
      <strong>and more like an open ocean.</strong>
    </div>
  </section>

  <section class="fields" id="explore">
    <div class="fields-intro">
      <div class="section-label reveal"><span>02</span> Explore</div>
      <h2 class="reveal">Every field is<br />worth <em>diving into.</em></h2>
      <p class="reveal">Follow your question wherever it leads. RESERA welcomes work across disciplines, methods, and borders.</p>
    </div>
    <div class="field-list">
      {#each fields as field}
        <article class="field-row reveal">
          <span class="field-number">{field.number}</span><h3>{field.title}</h3><p>{field.text}</p><span class="field-arrow">↗</span>
        </article>
      {/each}
    </div>
  </section>

  <section class="quote-panel" aria-label="Research philosophy">
    <div class="quote-mark">“</div>
    <blockquote class="reveal">Research is not about knowing<br />the answer. It is about being<br /><em>brave enough to look.</em></blockquote>
    <div class="depth-meter" aria-hidden="true"><span>0m</span><i></i><span>1,200m</span></div>
  </section>

  <Opportunities user={currentUser} onRequestAuth={() => authOpen = true} />

  <section class="process-section" id="process">
    <div class="process-heading">
      <div class="section-label reveal"><span>04</span> The process</div>
      <h2 class="reveal">From a spark<br />to something <em>real.</em></h2>
    </div>
    <div class="process-list">
      {#each process as item}
        <article class="process-item reveal"><span class="process-number">{item.step}</span><div><h3>{item.title}</h3><p>{item.text}</p></div></article>
      {/each}
    </div>
  </section>

  <section class="community">
    <div class="community-card reveal">
      <div class="community-glow" aria-hidden="true"></div>
      <p class="eyebrow"><span></span> The collective</p>
      <h2>Research is deeper<br />when we do it <em>together.</em></h2>
      <p>Meet students exploring ideas across science, technology, culture, and society. Trade feedback, join a project, or bring your own question to the table.</p>
      <a class="button button-light" href="https://discord.gg/kJWRfURJY3" target="_blank" rel="noreferrer">Join us on Discord <span>↗</span></a>
      <div class="community-stat"><strong>1,050+ members</strong><span>and growing across the world.</span></div>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="contact-top">
      <div class="section-label reveal"><span>05</span> Start here</div>
      <h2 class="reveal">What will<br /><em>you discover?</em></h2>
    </div>
    <div class="contact-bottom reveal">
      <p>Bring the question.<br />We’ll help you go deeper.</p>
      <div class="contact-links">
        <a href="mailto:reseraresearch1@gmail.com">Email us <span>↗</span></a>
        <a href="https://discord.gg/kJWRfURJY3" target="_blank" rel="noreferrer">Join Discord <span>↗</span></a>
        <a href="https://www.instagram.com/reseraa_a" target="_blank" rel="noreferrer">Instagram <span>↗</span></a>
      </div>
    </div>
  </section>
</main>

<footer>
  <a class="brand footer-brand" href="#home" aria-label="RESERA home">
    <span class="brand-mark footer-mark" style={`background-image: url('${asset('resera-logo.png')}')`}></span><span>RESERA</span>
  </a>
  <p>Student-led. Curiosity-driven.<br />Built for discovery.</p>
  <div class="footer-meta"><span>© {new Date().getFullYear()} RESERA</span><a href="#home">Back to the surface ↑</a></div>
</footer>

<AuthModal open={authOpen} user={currentUser} onClose={() => authOpen = false} onAuthenticated={(user) => currentUser = user} />
