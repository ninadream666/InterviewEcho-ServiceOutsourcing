<template>
  <el-dialog
    v-model="visible"
    :title="`开始 ${roleName} 面试`"
    width="550px"
    class="custom-clean-dialog"
    :show-close="false"
    destroy-on-close
  >
    <div class="space-y-8 py-2">
      <!-- Difficulty Selection -->
      <div>
        <label class="block text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">选择面试难度</label>
        <div class="grid grid-cols-3 gap-4">
          <button
            v-for="d in ['简单', '中等', '困难']"
            :key="d"
            @click="difficulty = d"
            :class="[
              'py-3 rounded-lg font-bold transition-colors border',
              difficulty === d 
                ? 'bg-[#E6F0FA] border-[#0066CC] text-[#0066CC]' 
                : 'bg-white border-gray-200 text-gray-600 hover:border-[#0066CC]'
            ]"
          >
            {{ d }}
          </button>
        </div>
      </div>

      <!-- Rounds Selection -->
      <div>
        <label class="block text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2 flex justify-between">
          面试轮次 (不含开场)
          <span class="text-[#0066CC]">{{ totalRounds }} 轮</span>
        </label>
        <div class="px-2">
          <el-slider 
            v-model="totalRounds" 
            :min="2" 
            :max="10" 
            :step="1"
            :marks="{ 2: '短', 6: '中', 10: '长' }"
          />
        </div>
      </div>

      <!-- Knowledge Points Selection -->
      <div>
        <label class="block text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">重点考察领域 (多选)</label>
        <div v-if="loading" class="flex items-center justify-center py-6">
          <el-icon class="is-loading text-[#0066CC] text-2xl"><Loading /></el-icon>
        </div>
        <div v-else-if="sections.length === 0" class="text-sm text-gray-400 py-2">
          该岗位暂无可选考察方向，面试官将按全流程进行。
        </div>
        <div v-else class="flex flex-wrap gap-3">
          <label 
            v-for="s in sections" 
            :key="s" 
            class="cursor-pointer"
            @click="toggleSection(s)"
          >
            <span 
              :class="[
                'px-4 py-2 rounded-lg border text-sm transition-all select-none block',
                selectedSections.includes(s)
                  ? 'bg-[#0066CC] text-white border-[#0066CC]'
                  : 'bg-white border-gray-200 text-gray-700 hover:border-[#0066CC]'
              ]"
            >
              {{ s }}
            </span>
          </label>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex gap-4 pt-2">
        <el-button @click="visible = false" class="!px-6 !border-gray-200 !text-gray-600 hover:!bg-gray-50">取消</el-button>
        <button 
          @click="handleConfirm" 
          class="flex-1 bg-[#0066CC] hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded transition-colors active:scale-[0.98]"
        >
          确认配置并进入房间
        </button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import api from '@/api'

const props = defineProps({
  roleName: String,
  roleKey: String
})

const emit = defineEmits(['confirm'])

const visible = ref(false)
const difficulty = ref('中等')
const totalRounds = ref(6)
const sections = ref([])
const selectedSections = ref([])
const loading = ref(false)

const open = async (roleKey) => {
  visible.value = true
  loading.value = true
  selectedSections.value = []
  
  const targetKey = roleKey || props.roleKey
  if (!targetKey) {
    loading.value = false
    return
  }

  try {
    const { data } = await api.get(`/interview/roles/${targetKey}/sections`)
    sections.value = data
  } catch (err) {
    console.error('Failed to fetch sections:', err)
  } finally {
    loading.value = false
  }
}

const toggleSection = (s) => {
  const idx = selectedSections.value.indexOf(s)
  if (idx > -1) {
    selectedSections.value.splice(idx, 1)
  } else {
    selectedSections.value.push(s)
  }
}

const handleConfirm = () => {
  emit('confirm', {
    difficulty: difficulty.value,
    knowledge_points: selectedSections.value,
    total_rounds: totalRounds.value
  })
  visible.value = false
}

defineExpose({ open })
</script>

<style>
.custom-clean-dialog {
  border-radius: 12px !important;
}
.custom-clean-dialog .el-dialog__header {
  border-bottom: 1px solid #F3F4F6;
  margin-right: 0;
  padding-bottom: 16px;
}
.custom-clean-dialog .el-dialog__title {
  font-weight: bold;
  color: #1F2937;
  font-size: 1.25rem;
}
</style>