-- upgrade --
CREATE TABLE IF NOT EXISTS `fm_user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '账号',
    `password` VARCHAR(128) NOT NULL  COMMENT '密码',
    `email` VARCHAR(254) NOT NULL  COMMENT '邮箱',
    `is_staff` BOOL NOT NULL  COMMENT '后台管理员' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='用户';
CREATE TABLE IF NOT EXISTS `fm_address` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `receiver` VARCHAR(20) NOT NULL  COMMENT '收件人',
    `addr` VARCHAR(256) NOT NULL  COMMENT '收件地址',
    `zip_code` VARCHAR(6)   COMMENT '邮政编码',
    `phone` VARCHAR(11) NOT NULL  COMMENT '手机号',
    `is_default` BOOL NOT NULL  COMMENT '是否默认' DEFAULT 0,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_fm_addre_fm_user_86c45b1a` FOREIGN KEY (`user_id`) REFERENCES `fm_user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='收货地址';
CREATE TABLE IF NOT EXISTS `fm_goods` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `name` VARCHAR(20) NOT NULL  COMMENT '商品SPU名称',
    `detail` LONGTEXT NOT NULL  COMMENT '商品详情'
) CHARACTER SET utf8mb4 COMMENT='商品SPU';
CREATE TABLE IF NOT EXISTS `fm_goods_type` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `name` VARCHAR(20) NOT NULL  COMMENT '种类名称',
    `logo` VARCHAR(20) NOT NULL  COMMENT '标识',
    `image` VARCHAR(254) NOT NULL  COMMENT '商品类型图片url'
) CHARACTER SET utf8mb4 COMMENT='商品种类';
CREATE TABLE IF NOT EXISTS `fm_goods_sku` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `name` VARCHAR(20) NOT NULL  COMMENT '商品名称',
    `desc` VARCHAR(256) NOT NULL  COMMENT '商品简介',
    `price` DECIMAL(10,2) NOT NULL  COMMENT '商品价格',
    `unite` VARCHAR(20) NOT NULL,
    `image` VARCHAR(256) NOT NULL  COMMENT '商品图片',
    `stock` INT NOT NULL  COMMENT '商品库存' DEFAULT 1,
    `sales` INT NOT NULL  COMMENT '商品销量' DEFAULT 0,
    `status` SMALLINT NOT NULL  COMMENT '商品状态((0, \'下线\'), (1, \'上线\'))' DEFAULT 1,
    `goods_id` INT NOT NULL COMMENT '商品SPU',
    `type_id` INT NOT NULL COMMENT '商品种类',
    CONSTRAINT `fk_fm_goods_fm_goods_a30eb4d4` FOREIGN KEY (`goods_id`) REFERENCES `fm_goods` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_fm_goods_fm_goods_81a09d61` FOREIGN KEY (`type_id`) REFERENCES `fm_goods_type` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='商品表';
CREATE TABLE IF NOT EXISTS `fm_goods_image` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `image` VARCHAR(256) NOT NULL  COMMENT '图片',
    `sku_id` INT NOT NULL,
    CONSTRAINT `fk_fm_goods_fm_goods_19f85186` FOREIGN KEY (`sku_id`) REFERENCES `fm_goods_sku` (`id`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4 COMMENT='商品图片';
CREATE TABLE IF NOT EXISTS `fm_index_banner` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `image` VARCHAR(254) NOT NULL  COMMENT '图片',
    `index` SMALLINT NOT NULL  COMMENT '展示顺序' DEFAULT 0,
    `sku_id` INT NOT NULL,
    CONSTRAINT `fk_fm_index_fm_goods_4ff8c018` FOREIGN KEY (`sku_id`) REFERENCES `fm_goods_sku` (`id`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4 COMMENT='首页轮播商品';
CREATE TABLE IF NOT EXISTS `fm_index_promotion` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `name` VARCHAR(20) NOT NULL  COMMENT '活动名称',
    `url` VARCHAR(254) NOT NULL  COMMENT '活动链接',
    `image` VARCHAR(254) NOT NULL  COMMENT '活动图片',
    `index` SMALLINT NOT NULL  COMMENT '展示顺序' DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='主页促销活动';
CREATE TABLE IF NOT EXISTS `fm_index_type_goods` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `display_type` SMALLINT NOT NULL  COMMENT '展示类型((0, \'标题\'), (1, \'图片\'))' DEFAULT 1,
    `index` SMALLINT NOT NULL  COMMENT '展示顺序' DEFAULT 0,
    `sku_id` INT NOT NULL COMMENT '商品SKU',
    `type_id` INT NOT NULL COMMENT '商品类型',
    CONSTRAINT `fk_fm_index_fm_goods_22e40f75` FOREIGN KEY (`sku_id`) REFERENCES `fm_goods_sku` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_fm_index_fm_goods_7d1ebd61` FOREIGN KEY (`type_id`) REFERENCES `fm_goods_type` (`id`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4 COMMENT='主页分类展示商品';
CREATE TABLE IF NOT EXISTS `fm_order_info` (
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `order_id` VARCHAR(128) NOT NULL  PRIMARY KEY COMMENT '订单ID',
    `pay_method` SMALLINT NOT NULL  COMMENT '((1, \'货到付款\'), (2, \'微信支付\'), (3, \'支付宝\'), (4, \'银联支付\'))' DEFAULT 3,
    `total_count` INT NOT NULL  COMMENT '商品数量' DEFAULT 1,
    `total_price` DECIMAL(10,2) NOT NULL  COMMENT '商品总价',
    `transit_price` DECIMAL(10,2) NOT NULL  COMMENT '订单运费',
    `order_status` SMALLINT NOT NULL  COMMENT '((1, \'待支付\'), (2, \'待发货\'), (3, \'待收货\'), (4, \'待评价\'), (5, \'已完成\'))订单状态' DEFAULT 1,
    `trade_no` VARCHAR(128) NOT NULL  COMMENT '支付编号' DEFAULT '',
    `addr_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_fm_order_fm_addre_af43119c` FOREIGN KEY (`addr_id`) REFERENCES `fm_address` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_fm_order_fm_user_cf1f5b2e` FOREIGN KEY (`user_id`) REFERENCES `fm_user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='订单详细';
CREATE TABLE IF NOT EXISTS `fm_order_goods` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_delete` BOOL NOT NULL  COMMENT '删除标记' DEFAULT 0,
    `count` INT NOT NULL  COMMENT '商品数量' DEFAULT 1,
    `price` DECIMAL(10,2) NOT NULL  COMMENT '商品单价',
    `comment` VARCHAR(256) NOT NULL  COMMENT '评论' DEFAULT '',
    `order_id` VARCHAR(128) NOT NULL,
    `sku_id` INT NOT NULL,
    CONSTRAINT `fk_fm_order_fm_order_9fbca578` FOREIGN KEY (`order_id`) REFERENCES `fm_order_info` (`order_id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_fm_order_fm_goods_cffa61fc` FOREIGN KEY (`sku_id`) REFERENCES `fm_goods_sku` (`id`) ON DELETE RESTRICT
) CHARACTER SET utf8mb4 COMMENT='订单商品';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
