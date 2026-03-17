-- 创建宠物知识表
CREATE TABLE pet_knowledge (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
);

-- 插入示例数据
INSERT INTO pet_knowledge (title, content, image_url) VALUES
('如何正确喂养猫咪', '猫咪的饮食需要注意营养均衡，不同年龄段的猫咪有不同的饮食需求。幼猫需要更多的蛋白质和热量，成年猫需要控制体重，老年猫需要易消化的食物。', 'https://example.com/cat-food.jpg'),
('狗狗的日常护理', '狗狗需要定期梳理毛发、修剪指甲、清洁耳朵和牙齿。不同品种的狗狗有不同的护理需求，比如长毛狗需要更频繁的梳理。', 'https://example.com/dog-care.jpg'),
('宠物疫苗接种指南', '宠物需要定期接种疫苗，以预防各种传染病。猫咪需要接种猫瘟、猫鼻支、猫杯状病毒等疫苗，狗狗需要接种狂犬病、犬瘟热、细小病毒等疫苗。', 'https://example.com/pet-vaccine.jpg'),
('如何训练宠物', '训练宠物需要耐心和 consistency。使用 positive reinforcement 方法，当宠物表现良好时给予奖励。训练应该从基础指令开始，如坐下、握手、过来等。', 'https://example.com/pet-training.jpg'),
('宠物健康检查', '定期带宠物去看兽医，进行健康检查。检查内容包括体重、体温、心率、呼吸、口腔健康、皮肤状况等。早期发现健康问题可以及时治疗，提高治愈率。', 'https://example.com/pet-checkup.jpg');