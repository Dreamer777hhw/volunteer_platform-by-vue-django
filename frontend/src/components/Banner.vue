<!-- 
    * @FileDescription: 轮播图组件，包含图片轮播、左右切换按钮和指示点功能
    * @Author: infinity
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
 -->

<template>
  <div class="banner-container">
    <div class="banner">
      <div class="banner-images">
        <img
          v-for="(image, index) in images"
          :key="index"
          :src="`/activity-images/${image.name}`"
          :alt="image.alt"
          :class="{ active: currentImage === index }"
          @click="navigateToDetail(image.link)"
        />
        <button class="prev" @click="prevImage">‹</button>
        <button class="next" @click="nextImage">›</button>
      </div>
      <div class="banner-dots">
        <span
          v-for="(image, index) in images"
          :key="index"
          :class="{ active: currentImage === index }"
          @click="goToImage(index)"
        ></span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'BannerComponent',
  data() {
    return {
      images: [
        // TODO: 选择合适的分辨率图片 从后端获取相应的数据
        // { name: 'banner-1.jpg', alt: 'Banner 1', link: '/activity/detail/ABCDEFG' },
        // { name: 'banner-2.jpg', alt: 'Banner 2', link: '/activity/detail/HIJKLMN' },
        // { name: 'banner-3.jpg', alt: 'Banner 3', link: '/activity/detail/OPQRSTU' },
        // { name: 'banner-4.jpg', alt: 'Banner 4', link: '/activity/detail/VWXYZAB' },
        // { name: 'banner-5.jpg', alt: 'Banner 5', link: '/activity/detail/CDEFGHI' },
      ],
      currentImage: 0,
      intervalId: null,
    };
  },
  methods: {
    async fetchUpcomingActivities() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/upcoming-activities/');
        // 假设返回的活动数据包含 activity_name 和 link
        this.images = response.data.map(activity => ({
          name: `${activity.name}.png`,
          alt: activity.name,
          link: activity.link
        }));
      } catch (error) {
        console.error("获取即将开始的活动失败:", error);
      }
    },
    /**
     * 切换到下一张图片
     */
    nextImage() {
      this.currentImage = (this.currentImage + 1) % this.images.length;
      this.resetAutoSlide();
    },
    /**
     * 切换到上一张图片
     */
    prevImage() {
      this.currentImage = (this.currentImage - 1 + this.images.length) % this.images.length;
      this.resetAutoSlide();
    },
    /**
     * 点击指示点跳转到对应图片
     * @param {number} index - 图片索引
     */
    goToImage(index) {
      this.currentImage = index;
      this.resetAutoSlide();
    },
    /**
     * 点击图片跳转到指定路径
     * @param {string} link - 跳转的路径
     */
    navigateToDetail(link) {
      this.$router.push(link);
    },
    /**
     * 开始自动轮播
     */
    startAutoSlide() {
      this.intervalId = setInterval(this.nextImage, 5000); // 每隔5秒切换
    },
    /**
     * 停止自动轮播
     */
    stopAutoSlide() {
      clearInterval(this.intervalId);
    },
    /**
     * 重置自动轮播计时器
     */
    resetAutoSlide() {
      this.stopAutoSlide();
      this.startAutoSlide();
    },
  },
  mounted() {
    this.startAutoSlide();
    this.fetchUpcomingActivities();
  },
  beforeUnmount() {
    this.stopAutoSlide(); 
  },
};
</script>

<style scoped>
.banner-container {
  justify-content: center;
}

.banner {
  position: relative;
  height: 330px;
  width: 1200px;
  overflow: hidden;
  border-radius: 15px; 
}

.banner-images {
  display: flex;
  width: 100%;
  height: 100%;
}

.banner-images img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: none;
  transition: opacity 0.5s ease-in-out;
  border-radius: 15px; 
}

.banner-images img.active {
  display: block;
}

.banner-images img.active {
  opacity: 1;
}

.banner-images img:not(.active) {
  opacity: 0;
}

.banner button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.3); /* 增加透明度 */
  color: white;
  border: none;
  height: 30px;
  width: 30px;
  cursor: pointer;
  z-index: 1;
  border-radius: 50%; 
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

.banner-dots {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.banner-dots span {
  width: 10px;
  height: 10px;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  cursor: pointer;
}

.banner-dots span.active {
  background-color: white;
}
</style>