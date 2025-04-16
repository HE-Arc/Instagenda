<script setup>
import axios from 'axios';
import { onMounted } from 'vue';
import router from '@/router'
import { useRoute } from 'vue-router';

const route = useRoute();
const code = route.query.code;

async function postCode() {
    const response = await axios.post('/ig/connection/', { code: code })
    return response.data
}

onMounted(async () => {
    await postCode()
    router.push('/user')
})
</script>
