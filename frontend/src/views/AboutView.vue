<template>
  <div class="container">
    <h1>INSTAGENDA</h1>

    <section>
      <p>
        <strong>Instagenda</strong> est une application web développée dans le cadre du cours HE-Arc
        <em>Développement Web II</em>. Elle permet de planifier des publications Instagram de manière collaborative,
        grâce à une interface simple et à l’intégration de l’API Meta Graph.
        L’application offre un système de gestion d’équipe, permettant au propriétaire du compte de travailler
        avec des community managers.
      </p>
    </section>

    <section>
      <h2>Technologies utilisées</h2>
      <ul>
        <li><strong>Frontend :</strong> Vue.js + Quasar</li>
        <li><strong>Backend :</strong> Django (REST Framework)</li>
        <li><strong>API :</strong> Meta Graph API (Instagram)</li>
      </ul>
    </section>

    <section>
      <h2>Équipe</h2>
      <ul>
        <li>Luan Bozier</li>
        <li>Eddy Naddeo</li>
        <li>Maxime Villarejo</li>
      </ul>
    </section>
  </div>
</template>

<style scoped>

.container {
  width: 80vw;
  margin: 0 auto;
  border-radius: 10px;
  background-color: #f8f9fa;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
  padding: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-align: center;
  color: #222;
}

h2 {
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #444;
}

ul {
  list-style: disc;
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}

p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}
</style>
