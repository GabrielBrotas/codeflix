import { Category } from "../../../domain/category/entities";
import CategoryRepository from "../../../domain/category/repository/category.repository";
import { CategoryOutput, CategoryOutputMapper } from "../../dto/category-output";
import {default as DefaultUseCase} from '../../use-case';

export namespace CreateCategoryUseCase {
  export class UseCase implements DefaultUseCase<Input, Output> {
    constructor(private categoryRepo: CategoryRepository.Repository) {}
  
    async execute(input: Input): Promise<Output> {
      const entity = new Category(input);
      await this.categoryRepo.insert(entity);
      return CategoryOutputMapper.toOutput(entity);
    }
  }

  export type Input = {
    name: string;
    description?: string;
    is_active?: boolean;
  };
  
  export type Output = CategoryOutput;
  
}

export default CreateCategoryUseCase;
